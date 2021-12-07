#!/bin/bash

INTERFACE_IP=/sbin/ifconfig $INTERFACE | egrep -o '([0-9]+[.]){3}[0-9]+' | head -n 1
nmap -sn $INTERFACE_IP/24
