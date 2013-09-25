#!/bin/bash

### daemons
# nm-applet: network manager
# gkrellm: system monitor
# diodon: clipboard manager
# arbtt-capture: arbitrary time tracker
# x-tile: window tiling
# To add: qamixer (well, some mixer); gnome-activity journal
for i in nm-applet gkrellm diodon arbtt-capture x-tile
do
    if which ${i}
    then
        if ! pidof ${i}
        then
            echo "not running: $i"
            ${i} &
        fi
    fi
done

# TODO: add workspace specific programs

# ssh-add
if [[ `ssh-add -l` != *id_?sa* ]]
then
 SSH_ASKPASS=/usr/bin/ksshaskpass
 if [[ -e $SSH_ASKPASS ]]
 then
   SSH_ASKPASS=${SSH_ASKPASS} ssh-add
 fi
fi