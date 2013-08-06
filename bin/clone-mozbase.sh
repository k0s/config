#!/bin/bash

VENV=virtualenv.py

if [[ -d "${VIRTUAL_ENV}" ]]
then
    echo "virtualenv: ${VIRTUAL_ENV}"
else
    if [ -n "${VIRTUAL_ENV}" ]
    then
        echo "VIRTUAL_ENV defined but not a directory: ${VIRTUAL_ENV}"
        exit 1
    fi

    if ! which ${VENV}
    then
        echo "${VENV} not found"
        exit 1
    fi
    VIRTUAL_ENV=${PWD}/mozbase
    echo "Creating virtualenv: ${VIRTUAL_ENV}"
    ${VENV} ${VIRTUAL_ENV}
    cd ${VIRTUAL_ENV}
    . bin/activate
    mkdir -p src
    cd src
fi

git clone git@github.com:k0s/mozbase.git
cd mozbase
git remote add mozilla git@github.com:mozilla/mozbase.git
git pull mozilla master
git push origin master

if [ -d "${VIRTUAL_ENV}" ]
then
    python setup_development.py
fi