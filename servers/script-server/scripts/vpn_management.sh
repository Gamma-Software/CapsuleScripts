#!/bin/bash

if [[ $CHOICE == "start" ]]
then
    echo $CHOICE
    service open vpn start
    service openvpn@client start
    exit
fi

if [[ $CHOICE == "stop" ]]
then
    echo $CHOICE
    service openvpn stop
    service openvpn@client stop
    exit
fi

if [[ $CHOICE == "restart" ]]
then
    echo $CHOICE
    service openvpn restart
    service openvpn@client restart
    exit
fi

