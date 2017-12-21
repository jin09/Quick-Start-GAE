#!/bin/bash
target=$1
tokill=$(docker ps | grep $target | cut -d " " -f1)
for k in "${tokill[@]}"
do
docker rm -f $k
done
docker rmi -f $target
docker build -t $target .
docker run -d -p 5000:8080 --restart always $target
new=$(docker ps | grep $target | cut -d " " -f1)
docker logs -f $new
