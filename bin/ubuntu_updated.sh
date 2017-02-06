#!/bin/bash

set -e

# script to update ubuntu
# Ref:
# http://mixeduperic.com/ubuntu/how-to-keep-your-ubuntu-server-updated-with-patches-and-security-fixes-using-the-command-line


if sudo apt-get update -y
then
    # -s = dry run
    # sudo apt-get -u -s -y upgrade

    sudo apt-get -u -y upgrade

    # TODO: sudo apt-get -u -s dist-upgrade

fi

# cleanup
sudo apt -y autoremove
