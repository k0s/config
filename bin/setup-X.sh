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
        if ! pidof -x ${i}
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
 GUI_SSH_ASKPASS=/usr/bin/ksshaskpass
 if [[ -e "${GUI_SSH_ASKPASS}" ]]
 then
   SSH_ASKPASS=${GUI_SSH_ASKPASS} ssh-add
 elif [[ -z "$PS1" ]]
 then
             # http://www.cyberciti.biz/faq/linux-unix-bash-check-interactive-shell/

   echo "not running ssh-add: PS1 not found"
 else
   ssh-add # interactive terminal
 fi
fi