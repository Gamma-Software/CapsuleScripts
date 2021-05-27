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
path_to_conf = os.path.join("/etc/imu_measure/config.yaml")
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
    filename="/var/log/imu_measure/" + dt.datetime.now().strftime("%Y%m%d-%H%M%S") + ".log",
    filemode="a",
    level=logging.DEBUG if conf["debug"] else logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
    datefmt='%m/%d/%Y %I:%M:%S %p')
sensor = vnpy.VnSensor()

# ----------------------------------------------------------------------------------------------------------------------
# Initiate MQTT variables
# ----------------------------------------------------------------------------------------------------------------------
client = mqtt.Client()
logging.info("Connect to localhost broker")
client.connect(conf["mqtt"]["host"], conf["mqtt"]["port"], 60)

while not client.is_connected():
    logging.info("Waiting 1 sec for the broker connection")
    time.sleep(1)

# ----------------------------------------------------------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------------------------------------------------------
try:
    while True:
        while sensor.verify_sensor_connectivity() and not sensor.is_connected:
            logging.info("Waiting 1 sec for the sensor to connect")
            sensor.response_timeout_ms = 1000
            sensor.connect(conf["serial"]["port"], conf["serial"]["baud"])
        logging.info("IMU sensor port open: " + conf["serial"]["port"] + " at baudrate " + conf["serial"]["baud"])
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
        logging.info("IMU sensor port disconnected: " + conf["serial"]["port"] + " at baudrate " + conf["serial"]["baud"])
        logging.info("Trying to reconnect")
except KeyboardInterrupt:
    logging.info("Stop script")
    sensor.disconnect()
    client.publish("/process/imu_measure/alive", False)
    client.disconnect()
    sys.exit(0)
