# [frontpage](frontpage/README.md)
This web page is the entrypoint of the user, It shortcuts all every user interface

# [script-server](script-server/README.md)
This web page give the user to operate the server

# [Trip Overview](trip-overview/README.md)
This web page give the user the overview of the trip

## How to start a server (via Docker) with a custom IP
(Instead of setting multiple server with a different port)

Docker exposes network services in containers through the use of port mappings, and port mappings can bind to specific ip addresses on your host. So if you want to have one web server at 192.168.10.10 and another webserver at 192.168.10.20, first make sure this addresses are available on your host:

ip addr add 192.168.10.10/24 dev eth0
ip addr add 192.168.10.20/24 dev eth0
Then start the first container:

docker run -p 192.168.10.10:80:80 mywebserver
And finally start the second container:

docker run -p 192.168.10.20:80:80 mywebserver
In the above commands, the -p option is used to bind the port mapping to a particular ip address. Now you have two containers offering a service on the same port (port 80) but on different ip addresses.
