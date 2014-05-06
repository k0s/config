#!/bin/bash

PID=$$

echo "The PID of this shell script is ${PID}"
ps auxwww | grep ${PID}

if which tempfile
then
    PIDFILE=$(tempfile)
    echo "PID file: ${PIDFILE}"
    echo ${PID} > ${PIDFILE}
    kill $(cat ${PIDFILE})
fi

kill ${PID}