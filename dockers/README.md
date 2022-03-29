# Docker tig
tig = Telegraf Influxdb Grafana
this is a tool set to capture/store/plot data from the server
## Prerequisite
A mosquitto 
docker-compose installed on the host by following https://docs.docker.com/compose/install/

### Mosquitto server
The mosquitto server is a lightweight MQTT broker that runs on the host. It is used to send/receive messages between the docker containers. 
To view the mosquitto values, you can run the docker image:
`docker run -e "TZ=Europe/Paris" -v "/home/rudloff/sources/CapsuleScripts/dockers/mqtt-explorer/:/mqtt-explorer/config" -p "4444:4000" smeagolworms4/mqtt-explorer`
## Run
This is simple, just run
`docker-compose up -d`
in the folder where the docker-compose.yaml is stored

# OpenStreetMap offline server
## Download OSM map
To run your own server download the osm map at [osm_map_link](https://data.maptiler.com/download/WyI5MWFkZGQwNS1hYTA3LTQ1MzctYWU3Yi1lZDI2OGQ5YTJkNmMiLCItMSIsNzkwMV0.YO1_Iw.X58ryoOVoSxb_ATt48yjiMXZTp0/maptiler-osm-2017-07-03-v3.6.1-planet.mbtiles?usage=personal) running the command `sudo wget -c https://data.maptiler.com/download/WyI5MWFkZGQwNS1hYTA3LTQ1MzctYWU3Yi1lZDI2OGQ5YTJkNmMiLCItMSIsNzkwMV0.YO1_Iw.X58ryoOVoSxb_ATt48yjiMXZTp0/maptiler-osm-2017-07-03-v3.6.1-planet.mbtiles?usage=personal -O path_to_osm.mbtiles &`

## Run and setup offline map
Prerequisite: Docker installed
This is very simple just run the command `docker run -p 8080:80 -d --restart unless-stopped -v /mnt/data/osm_maps/osm.mbtiles:/data/osm.mbtiles --name osm_offline_map store/klokantech/openmaptiles-server-dev:1.4-free`\
Then go to https://localhost:8080/ and follow the setup instructions


## Samba shares
docker run -dt -v /mnt/data/shares/:/mnt/data/shares -v /etc/samba/smb.conf:/etc/samba/smb.conf -p 445:445 --name samba --restart=always stanback/alpine-samba --no-process-group

## DNS server
https://github.com/MatthewVance/unbound-docker
The DNS server is used to attribuate as host name to an ip in order to resolve its name.