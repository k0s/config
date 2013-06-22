#!/bin/bash

# process environment
# list process environment variables

# must be run as root
if [[ "$(whoami)" != "root" ]]
then
    echo "must be run as root"
    exit 1
fi

# loop over arguments
for PROG in $@
do
    EXIT=0
    if PID=$(pidof -x ${PROG})
    then
        echo '='${PROG}: ${PID}'='
        cat /proc/${PID}/environ | tr '\000' '\012' | sort
    else
        EXIT=1
        echo ""
    fi
done