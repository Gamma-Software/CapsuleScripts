#!/bin/bash
#docker ps | grep travelblog
#if [ $? -eq 1 ]; then
#    echo -e "Le blog n'est pas démarré, il n'y a pas d'intérêt à mettre à jour les medias"
#    exit 1
#fi
#docker ps | grep blog-editor
#if [ $? -eq 1 ]; then
#    echo -e "L'editeur n'est pas démarré, il n'y a pas d'intérêt à mettre à jour les medias"
#    exit 1
#fi

#rsync -ra /mnt/data/shares/data/ /home/rudloff/sources/CapsuleScripts/servers/travelblog/images
cd /home/rudloff/sources/CapsuleScripts/servers/travelblog
eval "$(ssh-agent -s)"
ssh-add /home/rudloff/.ssh/id_ed25519
git config --global --add safe.directory '*'
git fetch --all
git pull
echo "Les medias pour le blog sont synchronisés"
