#!/bin/bash
rsync -ra /mnt/data/shares/data/ /home/rudloff/sources/CapsuleScripts/servers/travelblog/images
echo "Les medias pour le blog sont synchronisés"

docker ps | grep travelblog
if [ $? -eq 0 ]; then
    echo "Le blog est déjà en cours d'édition et disponible à l'adresse suivante http://capsule.local:5000"
else
    #docker run -d --name travelblog -p 5000:4000 -v "/home/rudloff/sources/CapsuleScripts/servers/travelblog:/srv/jekyll" jekyll/jekyll:3.8 jekyll serve --watch --force_polling --verbose --trace --livereload
    docker start travelblog
    docker ps | grep travelblog
    if [ $? -eq 1 ]; then
        echo -e "Le site n'a pas démarré correctement, on force le démarrage."
        docker run -d --name travelblog -p 5000:4000 -v "/home/rudloff/sources/CapsuleScripts/servers/travelblog:/srv/jekyll" jekyll/jekyll:3.8 jekyll serve --watch --force_polling --verbose --trace --livereload
        sleep 10
    fi
    echo -e "Le blog est lancé et disponible dans quelques minutes à l'adresse suivante sur http://capsule.local:5000"
    echo -e "le blog n'est disponible que dans le reseau local et n'est pas partagé au monde entier."    
fi

docker ps | grep blog-editor
if [ $? -eq 0 ]; then
    echo "L'editeur du blog est déjà en cours d'édition et disponible à l'adresse suivante http://capsule.local:9888"
else
    #docker run -d --name blog-editor -p 9888:8080 -v "/home/rudloff/sources/CapsuleScripts/dockers/blog-editor/config:/home/coder/.config" -v "/home/rudloff/sources/CapsuleScripts/servers/travelblog:/home/coder/project" -u "1000:1000" -e "DOCKER_USER=$USER" codercom/code-server:latest
    docker start blog-editor
    docker ps | grep blog-editor
    if [ $? -eq 1 ]; then
        echo -e "L'editeur n'est pas démarré correctement, on force le démarrage."
	docker run -d --name blog-editor -p 9888:8080 -v "/home/rudloff/.ssh:/home/coder/.ssh"  -v "/home/rudloff/sources/CapsuleScripts/dockers/blog-editor/config:/home/coder/.config" -v "/home/rudloff/sources/CapsuleScripts/servers/travelblog:/home/coder/project" -u "1000:1000" -e "DOCKER_USER=$USER" codercom/code-server:latest
	sleep 10
    fi
    echo -e "Son edition est possible sur http://capsule.local:9888"
    echo -e "Le mot de passe est $(grep "password:" /home/rudloff/sources/CapsuleScripts/dockers/blog-editor/config/code-server/config.yaml)"
fi
