#!/bin/bash

# http://blog.yohanliyanage.com/2015/05/docker-clean-up-after-yourself/

# Make sure exited containers are deleted
docker rm -v $(docker ps -a -q -f status=exited)

# Remove unwanted 'dangling' images
docker rmi $(docker images -f "dangling=true" -q)

# Remove unwanted volumes
docker volume rm $(docker volume ls -qf dangling=true)

# TODO: remove stopped containers
# docker container prune -f
