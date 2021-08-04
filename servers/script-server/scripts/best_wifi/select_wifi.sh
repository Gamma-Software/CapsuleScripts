#!/bin/bash

GetWifis () {
    nmcli dev wifi list
}
GetWifisSimple () {
    nmcli -f ssid dev wifi | sed '1 d'
}
SetWifi () {
    echo "Connecting to " $WIFI
    # If the connection is ethablished
    if nmcli --ask dev wifi connect $WIFI; then
        echo "Performing speed test on " $WIFI
        
        #speedtest I don’t know why but this fails to execute
    fi
}
if [ ${1} = "simple_list" ]
then
    GetWifisSimple
    exit
fi

if [ ${1} = "detailed_list" ]
then
    GetWifis
    exit
fi

SetWifi
exit