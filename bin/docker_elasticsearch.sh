#!/bin/bash


export MACHINE=default
eval "$(docker-machine env default)"
export CIDFILE=$(mktemp -u)
docker run -P --cidfile ${CIDFILE} elasticsearch &
sleep 10

script_shutdown() {
    echo "**** Shutting down... ****"
   # http://unix.stackexchange.com/questions/55558/how-can-i-kill-and-wait-for-background-processes-to-finish-in-a-shell-script-whe
    docker kill `cat ${CIDFILE}`
}

trap 'script_shutdown' INT
export DOCKER_IP=$(docker-machine ip default)
export CONTAINER_PORT=$(docker port `cat ${CIDFILE}` | grep 9200 | sed 's/.*://')
export ELASTICSEARCH_URL="http://${DOCKER_IP}:${CONTAINER_PORT}/"
open ${ELASTICSEARCH_URL}
wait

