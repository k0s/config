#!/usr/bin/env bash

set -exuo pipefail

PYTHON_VERSION="3.7"

# TODO: take this from "$1"
DEST="${HOME}/web3"
rm -rf "${DEST}"

mkdir -p "${DEST}"
cd "${DEST}"
pyenv install "${PYTHON_VERSION}"
pyenv local "${PYTHON_VERSION}"
python --version
