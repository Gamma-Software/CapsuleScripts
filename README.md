# CapsuleScripts
Gather the different scripts for Capsule

## [Docker images](dockers/README.md)
Telegraf/Influxdb/Grafana docker-compose

## [Devices drivers](devices_driver/README.md)
This gather devices drivers such as GPS receiver for gps coordinates, IMU for acceleration inclination, CAN Decoder, USB Driver 

## [Servers](servers/README.md)
All the servers to interact with the user, such as frontpage, script-server, trip overview

# Distant Connection
## How to ssh tunneling
The Capsule server is connected to the Capsule local network. The camera is also connected to the Capsule local network. When connected remotely to access to another local device to its web interface like the Camera you should ssh tunnel the connection to a specific port as such:
```
ssh -L <destination_port>:<ip_to_fwd>:<port_to_fwd> remote_user@remote_host
```