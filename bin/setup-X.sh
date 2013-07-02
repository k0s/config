#!/bin/bash

# daemons
for i in nm-applet gkrellm diodon
do
    if ! ps aux | grep ${i} | grep -v 'grep'
    then
        echo "not running: $i"
        if which ${i}
        then
            ${i} &
        fi
    fi
done