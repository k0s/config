#!/usr/bin/env bash

# This script installs the k0s.org web server in a virtual environment
# in the directory specified by the first argument.

# Example usage:
# install-k0s-web.sh "${HOME}"/web2

set -euo pipefail

PYTHON_VERSION="3.7"

# Get DEST from "$1"
# DEST="${HOME}/web3"
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <destination>"
    exit 1
fi
DEST="$1"
if [ "${DEST:0:1}" != "/" ]
then
    echo "Destination must be an absolute path"
    exit 1
fi
beginswith() { case $2 in "$1"*) true;; *) false;; esac; }
if ! beginswith "${HOME}" "${DEST}"
then
    echo "Destination must be under your home directory"
    exit 1
fi

set -x

rm -rf "${DEST}"

# Make a directory for k0s.org web
mkdir -p "${DEST}"
cd "${DEST}"

# Install the proper version of Python with pyenv
# See https://github.com/pyenv/pyenv/wiki#suggested-build-environment
pyenv install --skip-existing "${PYTHON_VERSION}"
pyenv local "${PYTHON_VERSION}"
python --version

# Create a virtual environment
python -m venv .

# Activate the virtual environment
. bin/activate

# Install the required packages
bin/pip install --upgrade pip
bin/pip install -r "${HOME}"/web/requirements.txt

# echo command to run the server
set +x
command="sudo ${DEST}/bin/paster serve /home/jhammel/web/paster-wsgintegrate.ini"
echo "Run with:"
echo "${command}"
