#!/bin/bash -x

# see http://www.howtogeek.com/168147/add-public-ssh-key-to-remote-server-in-a-single-command/

KEY=~/.ssh/id_rsa.pub

for arg in $@
do
    cat "${KEY}" | ssh ${arg} 'cat >> .ssh/authorized_keys'
done
