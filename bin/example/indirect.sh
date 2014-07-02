#!/bin/bash

NAME=foo
PASSWORD=bar
IP_ID=91
ENV=prod

for i in NAME PASSWORD IP_ID ENV
do
    echo "export $i=\"$(eval echo \$$i)\""
done
