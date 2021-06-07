import io
import os
import yaml
import sys
import pynmea2
import serial
import time
import logging
import datetime as dt
import paho.mqtt.client as mqtt


# ----------------------------------------------------------------------------------------------------------------------
# Read script parameters
# ----------------------------------------------------------------------------------------------------------------------
path_to_conf = os.path.join("/etc/capsule/gps_measure/config.yaml")
# If the default configuration is not install, then configure w/ the default one
if not os.path.exists(path_to_conf):
    sys.exit("Configuration file %s does not exists. Please reinstall the app" % path_to_conf)
# load configuration
with open(path_to_conf, "r") as file:
    conf = yaml.load(file, Loader=yaml.FullLoader)

# ----------------------------------------------------------------------------------------------------------------------
# Initiate variables
# ----------------------------------------------------------------------------------------------------------------------
connected = False
logging.basicConfig(
    filename="/var/log/capsule/gps_measure/" + dt.datetime.now().strftime("%Y%m%d-%H%M%S") + ".log",
    filemode="a",
    level=logging.DEBUG if conf.debug else logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
    datefmt='%m/%d/%Y %I:%M:%S %p')

# ----------------------------------------------------------------------------------------------------------------------
# Initiate MQTT variables
# ----------------------------------------------------------------------------------------------------------------------
# MQTT methods
def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    logging.info("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt

client = mqtt.Client()
logging.info("Connect to localhost broker")
client.username_pw_set(conf["mqtt"]["user"], conf["mqtt"]["pass"])
client.on_connect = on_connect  # Define callback function for successful connection
client.connect(conf["mqtt"]["host"], conf["mqtt"]["port"])
client.loop_start()

while not client.is_connected():
    logging.info("Waiting for the broker connection")
    time.sleep(1)

# ----------------------------------------------------------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------------------------------------------------------
client.publish("/process/gps_measure/alive", True)
while True:
    try:
        with serial.Serial(conf["gps_serial_port"], conf["gps_serial_baudrate"], timeout=1) as ser:
            logging.info("Opening port: " + conf["gps_serial_port"] + " at speed: " + conf["gps_serial_baudrate"])
            # 'warm up' with reading some input
            for i in range(5):
                logging.info("Dry run:"+str(ser.readline()))
            sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser), encoding='ascii', errors='ignore')
            last_valid_nmea = pynmea2.parse("$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D")
            while True:
                start_time = time.time()
                try:
                    nmeaobj = pynmea2.parse(sio.readline())
                    logging.debug(repr(nmeaobj))
                    if isinstance(nmeaobj, pynmea2.types.RMC) or isinstance(nmeaobj, pynmea2.types.GGA):
                        data = nmeaobj
                        if not data.is_valid:
                            logging.warning("GPS is not fixed")
                            client.publish("/gps_measure/fixed", False)
                        else:
                            client.publish("/gps_measure/fixed", True)
                            try:
                                if isinstance(last_valid_nmea, pynmea2.types.GGA):
                                    client.publish("/gps_measure/timestamp", dt.datetime.now().timestamp())
                                    client.publish("/gps_measure/latitude", round(data.latitude, 4))
                                    client.publish("/gps_measure/longitude", round(data.longitude, 4))
                                    client.publish("/gps_measure/speed", round(float(data.data[6]) * 1.852, 2))
                                    client.publish("/gps_measure/route", data.data[7])
                                if isinstance(last_valid_nmea, pynmea2.types.RMC):
                                    client.publish("/gps_measure/altitude", data.altitude)
                                last_valid_nmea = nmeaobj
                            except AttributeError as e:
                                logging.warning("Error on attribute {}".format(e))
                                pass
                except pynmea2.ParseError as e:
                    logging.warning('Parse error: {}'.format(e))
                    logging.warning("Retry getting a correct NMEA data")
                    pass
                except KeyboardInterrupt:
                    logging.info("Stop script")
                    client.publish("/process/gps_measure/alive", False)
                    client.disconnect()
                    sys.exit(0)
                client.publish("/process/gps_measure/alive", True)
                elapsed_time = conf["period_s"] - (time.time() - start_time)
                if elapsed_time > 0.0:
                    logging.info("Sleeps "+str(elapsed_time))
                    time.sleep(elapsed_time)
                else:
                    logging.warn("Execution time exceeds expected period: "+str(elapsed_time)+">"+conf["period_s"])
    except serial.SerialException as e:
        logging.error('Device error: {}'.format(e))
        client.publish("gps/process/alive", False)
        sys.exit('Device error: {}'.format(e))
