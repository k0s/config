#!/bin/bash

# stress test a program

export I=0
while "$@"
do
    echo ${I}
    I=$((I+1))
    sleep 5
done
