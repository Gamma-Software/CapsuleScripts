#!/bin/bash

docker ps | grep blog-editor
if [ $? -eq 0 ]; then
    docker stop blog-editor
fi
docker ps | grep travelblog
if [ $? -eq 0 ]; then
    docker stop travelblog
fi

echo "Le blog est stoppé et l'edition n'est plus possible"