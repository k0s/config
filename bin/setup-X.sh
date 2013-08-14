#!/bin/bash

# daemons
for i in nm-applet gkrellm diodon # 'synapse -s'
# To add: x-tile; qamixer (well, some mixer); gnome-activity journal
do
    if ! pidof ${i}
    then
        echo "not running: $i"
        if which ${i}
        then
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
   ssh-add
 fi
fi