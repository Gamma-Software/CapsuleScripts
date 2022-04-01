#!/bin/bash

docker ps | grep blog-editor
if [ $? -eq 0 ]; then
    docker stop blog-editor
    echo -e "Le blog est lancé et disponible dans quelques minutes à l'adresse suivante sur http://capsule.local:5000"
    echo -e "le blog n'est disponible que dans le reseau local et n'est pas partagé au monde entier."    
else
    echo "L'editeur du blog n'est pas lancé. Il faut la lancer avec le script Demarrer le blog et l'edition"
fi
docker ps | grep travelblog
if [ $? -eq 0 ]; then
    echo -e "Son edition est possible sur http://capsule.local:9888"
    echo -e "Le mot de passe est $(grep "password:" /home/rudloff/sources/CapsuleScripts/dockers/blog-editor/config/code-server/config.yaml)"
else
    echo "Le blog n'est pas lancé. Il faut la lancer avec le script Demarrer le blog et l'edition"
fi