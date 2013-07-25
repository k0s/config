#!/bin/bash

# daemons
for i in nm-applet gkrellm diodon # 'synapse -s'
# To add: x-tile; qamixer (well, some mixer); gnome-activity journal
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

# TODO: add workspace specific programs
