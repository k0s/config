#!/bin/bash

BASEDIR=${HOME}/cisco/log
STAMP=$(date +"%Y%m%d")
FILENAME="${BASEDIR}/${STAMP}.txt"

if [[ -e "${FILENAME}" ]]
then
    echo "emacs -nw +`wc -l ${FILENAME}` ${FILENAME}"
    emacs -nw +`wc -l "${FILENAME}"`
else
    emacs -nw ${FILENAME}
fi
