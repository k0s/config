#!/usr/bin/env bash

set -exuo pipefail

PYTHON_VERSION="3.7"

# TODO: take this from "$1"
DEST="${HOME}/web3"
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
command="sudo ${DEST}/bin/paster serve /home/jhammel/web/paster-wsgintegrate.ini"
echo "Run with:"
echo "${command}"
