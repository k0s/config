#!/bin/bash

title=$1
shift

if [[ "${title}" == ""  || "$#" == "0" ]]
then
    exit 1
fi

filename=~/web/site/comedy/cheapshots/${title}.txt

echo "$@" > ${filename}