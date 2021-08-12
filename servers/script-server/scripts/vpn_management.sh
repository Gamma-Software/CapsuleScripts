#!/bin/bash

if [ $CHOICE = "start" ]
then
    service openvpn start
    service openvpn@client start
    exit
fi

if [ $CHOICE = "stop" ]
then
    service openvpn stop
    service openvpn@client stop
    exit
fi

if [ $CHOICE = "restart" ]
then
    service openvpn restart
    service openvpn@client restart
    exit
fi

