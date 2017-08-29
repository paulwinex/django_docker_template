#!/bin/bash

# build project image
docker build -f Dockerfile_web -t paulwinex/project .

# build worker image from project image
docker build -f Dockerfile_workers -t paulwinex/worker .

#build scheduler image from project image
docker build -f Dockerfile_scheduler -t paulwinex/scheduler .

#build nginx 
docker build -t paulwinex/nginx_lua ./nginx

#init database
set -o allexport
source .env
set +o allexport
docker-compose up -d db
echo "Waiting 5 sec..."
sleep 10
docker-compose down



