Gather the different scripts and web apps and infrastructure as code for Capsule2024.

# What is Capsule2024 ?

Capsule2024 is a project started by my parents to make a round trip all around the world. They constructed and furnished their 4x4 car for them to sleep anywhere on land and still make their way through difficult road. The roadtrip will start in 2024.
As an engineer I wanted to be part of their journey and start building an IT project around it. They want to share their trip along the way and I have some ideas.

## Functionnalities
- Track the car and its behaviour to automatically construct a map gethering the travel informations, such as the number of country traveled, number of days since the start, the current path and location and roadtrip steps.
- Share the pictures taken by the travelers and put them onto the map
- Take an automatic movie of the current steps and create a timelapse shareable on social media and obviously on the map generated automatically
- Monitor the car and the solar panel
- Add an alarm system
- Host the travel blog to edit it then publish it on the web host server (which is my own home server)

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
