#!/bin/bash

VENV=virtualenv.py

if [[ -d "${VIRTUAL_ENV}" ]]
then
    echo "virtualenv: ${VIRTUAL_ENV}"
fi

git clone git@github.com:k0s/mozbase.git
cd mozbase
git remote add mozilla git@github.com:mozilla/mozbase.git
git pull mozilla master
git push origin master