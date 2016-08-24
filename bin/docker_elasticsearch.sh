#!/bin/bash

# run an ephemeral elasticsearch

# variables
export IMAGE="elasticsearch"
export PORT=9200

# Run docker with a CID file so we can attach to it
export CIDFILE=$(mktemp -u)
docker run -P --cidfile "${CIDFILE}" "${IMAGE}" &
sleep 10

# ensure we can shutdown properly
script_shutdown() {
    echo "**** Shutting down... ****"
   # http://unix.stackexchange.com/questions/55558/how-can-i-kill-and-wait-for-background-processes-to-finish-in-a-shell-script-whe
    docker kill `cat ${CIDFILE}`
}
trap 'script_shutdown' INT

# open the elasticsearch URL
export ELASTICSEARCH_URL="http://$(docker port `cat "${CIDFILE}"` ${PORT})/"
echo ${ELASTICSEARCH_URL}
open "${ELASTICSEARCH_URL}"

wait

