# Description
This script permits to select the best wifi

# Installation
You can launch it with this command /usr/bin/python3 /home/rudloff/source/CapsuleScripts/misc/best_wifi/best_wifi.py

or automatically launch it with crontab with this command
echo "$(echo "0 1 * * * /usr/bin/python3 /home/rudloff/source/CapsuleScripts/misc/best_wifi/best_wifi.py >> /var/log/capsule/best_wifi.log 2>&1";crontab -l 2>&1)" | crontab -