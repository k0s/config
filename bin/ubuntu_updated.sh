#!/bin/bash

# script to see if ubuntu is up to date

# -s = dry run
if apt-get update -y
then
    apt-get -u -s upgrade
fi
