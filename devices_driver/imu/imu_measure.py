import io
import os
import yaml
import sys
import time
import logging
import datetime as dt

import vnpy
import paho.mqtt.client as mqtt


# ----------------------------------------------------------------------------------------------------------------------
# Read script parameters
# ----------------------------------------------------------------------------------------------------------------------
path_to_conf = "/etc/capsule/imu_measure/config.yaml"
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
    filename="/var/log/capsule/imu_measure/" + dt.datetime.now().strftime("%Y%m%d-%H%M%S") + ".log",
    filemode="a",
    level=logging.DEBUG if conf["debug"] else logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
    datefmt='%m/%d/%Y %I:%M:%S %p')
sensor = vnpy.VnSensor()

# ----------------------------------------------------------------------------------------------------------------------
# Initiate MQTT variables
# ----------------------------------------------------------------------------------------------------------------------
# MQTT methods
def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    logging.info("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt

client = mqtt.Client()
logging.info("Connect to localhost broker")
client.username_pw_set("rudloff", "y4uv3jpc")
client.on_connect = on_connect  # Define callback function for successful connection
client.connect(conf["mqtt"]["host"], conf["mqtt"]["port"])
client.loop_start()

logging.info("Connection to Mosquitto Broker: " + conf["mqtt"]["host"] + " at baudrate " + str(conf["mqtt"]["port"]))

while not client.is_connected():
    logging.info("Waiting 1 sec for the broker connection")
    time.sleep(1)

# ----------------------------------------------------------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------------------------------------------------------
try:
    while True:
        while not sensor.is_connected:
            logging.info("Waiting 1 sec for the sensor to connect")
            logging.info("Trying to connect to IMU sensor with: " + conf["serial"]["port"] + " at baudrate " + str(conf["serial"]["baud"]))
            sensor.response_timeout_ms = 1000
            #sensor.connect(conf["serial"]["port"], conf["serial"]["baud"])
            sensor.connect("/dev/ttyUSB0", 921600)
            time.sleep(1)
        logging.info("IMU sensor port open: " + conf["serial"]["port"] + " at baudrate " + str(conf["serial"]["baud"]))
        while sensor.is_connected:
            client.publish("/process/imu_measure/alive", True)
            start_time = time.time()
            accel = sensor.read_acceleration_measurements()
            ypr = sensor.read_yaw_pitch_roll()
            elapsed_time = conf["period_s"] - (time.time() - start_time)
            client.publish("imu_measure/ypr", ypr, retain=True)
            if elapsed_time > 0.0:
                logging.info("Sleeps "+str(elapsed_time))
                time.sleep(elapsed_time)
            else:
                logging.warn("Execution time exceeds expected period: "+str(elapsed_time)+">"+conf["period_s"])
        logging.info("IMU sensor port disconnected: " + conf["serial"]["port"] + " at baudrate " + str(conf["serial"]["baud"]))
        logging.info("Trying to reconnect")
except KeyboardInterrupt:
    logging.info("Stop script")
    sensor.disconnect()
    client.publish("/process/imu_measure/alive", False)
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
