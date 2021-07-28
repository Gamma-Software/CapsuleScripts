# IMU measure
Gather the scripts for Capsule

# Installation
Create a python virtual environnement: 'virtualenv .venv"
Install requirements 'pip install .'
Install the configurations and service and udev rule 'python3 (from the virtualenv) install.py'
Change default user and pass config in /etc/capsule/imu_measure/config.yaml

# Docker image
## Build
`docker build .%`

# Run
`docker run -d --device=/dev/ttyUSB0 --restart=unless-stopped imu_measure:latest`

# Mosquitto publish topics
process/imu_measure/alive
imu_measure/attitude/yaw
imu_measure/attitude/pitch
imu_measure/attitude/roll
imu_measure/acceleration/x
imu_measure/acceleration/y
imu_measure/acceleration/z
imu_measure/leveled