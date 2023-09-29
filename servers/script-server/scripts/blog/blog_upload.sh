#!/bin/bash
cd /home/rudloff/sources/CapsuleScripts/servers/travelblog
eval "$(ssh-agent -s)"
ssh-add /home/rudloff/.ssh/id_ed25519
git config --global --add safe.directory /home/rudloff/sources/CapsuleScripts/servers/travelblog
git commit -am "update_site"
git push
echo "Les medias pour le blog sont synchronisés"
