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
    filename="/var/log/capsule/gps_driver.log",
    filemode="a",
    level=logging.DEBUG if conf["debug"] else logging.INFO,
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
client.publish("process/gps_measure/alive", True)
try:
    while True:
        try:
            with serial.Serial(conf["serial"]["port"], conf["serial"]["baud"], timeout=conf["serial"]["timeout"]) as read_gps:
                logging.info("GPS sensor port open: " + conf["serial"]["port"] + " at baudrate " + str(conf["serial"]["baud"]))
                # 'warm up' with reading some input
                for i in range(5):
                    logging.info("Dry run:"+str(read_gps.readline()))
                sio = io.TextIOWrapper(io.BufferedRWPair(read_gps, read_gps), encoding='ascii', errors='ignore')
                last_valid_nmea = pynmea2.parse("$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D")
                while read_gps.is_open:
                    client.publish("process/gps_measure/alive", True)
                    start_time = time.time()
                    try:
                        nmeaobj = pynmea2.parse(sio.readline())
                        logging.debug(repr(nmeaobj))
                        if isinstance(nmeaobj, pynmea2.types.RMC) or isinstance(nmeaobj, pynmea2.types.GGA):
                            data = nmeaobj
                            if not data.is_valid:
                                logging.warning("GPS is not fixed")
                                client.publish("gps_measure/fixed", False, retain=True)
                            else:
                                client.publish("gps_measure/fixed", True, retain=True)
                                try:
                                    if isinstance(last_valid_nmea, pynmea2.types.GGA):
                                        client.publish("gps_measure/latitude", round(data.latitude, 4), retain=True)
                                        client.publish("gps_measure/longitude", round(data.longitude, 4), retain=True)
                                        client.publish("gps_measure/speed", round(float(data.data[6]) * 1.852, 2), retain=True)
                                        client.publish("gps_measure/route", data.data[7], retain=True)
                                    if isinstance(last_valid_nmea, pynmea2.types.RMC):
                                        client.publish("gps_measure/altitude", data.altitude, retain=True)
                                    last_valid_nmea = nmeaobj
                                except AttributeError as e:
                                    logging.warning("Error on attribute {}".format(e))
                                    pass
                    except pynmea2.ParseError as e:
                        logging.error('Parse error: {}'.format(e))
                        logging.info("Retry getting a correct NMEA data")
                        pass
                    elapsed_time = conf["period_s"] - (time.time() - start_time)
                    if elapsed_time > 0.0:
                        time.sleep(elapsed_time)
        except serial.SerialException as e:
            logging.error('Device error: {}'.format(e))
            logging.info("Retry connecting to serial port after 1s of wait")
            time.sleep(1)
            pass
except KeyboardInterrupt:
    pass
logging.info("Stop script")
client.publish("process/gps_measure/alive", False)
client.loop_stop()
client.disconnect()
sys.exit(0)
