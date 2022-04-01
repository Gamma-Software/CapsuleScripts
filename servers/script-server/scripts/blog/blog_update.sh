#!/bin/bash
docker ps | grep travelblog
if [ $? -eq 1 ]; then
    echo -e "Le blog n'est pas démarré, il n'y a pas d'intérêt à mettre à jour les medias"
    exit 1
fi
docker ps | grep blog-editor
if [ $? -eq 1 ]; then
    echo -e "L'editeur n'est pas démarré, il n'y a pas d'intérêt à mettre à jour les medias"
    exit 1
fi

rsync -ra /mnt/data/shares/data/ /home/rudloff/sources/CapsuleScripts/servers/travelblog/images
echo "Les medias pour le blog sont synchronisés"