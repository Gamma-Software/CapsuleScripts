# Description
This script permits to clear the cache and the swap cache

# Installation
You can launch it with this command sh /home/rudloff/source/CapsuleScripts/misc/clear_cache/clearcache.py

or automatically launch it with crontab with this command
echo "$(echo "0 1 * * * sh /home/rudloff/source/CapsuleScripts/misc/clear_cache/clearcache.py >> /var/log/capsule/clear_cache.log 2>&1";crontab -l 2>&1)" | crontab -