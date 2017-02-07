#!/bin/bash

set -e

cd

silvermirror
hg pull

set +e
hg push  # will exit 1 on no changes found
set -e

ubuntu_updated.sh
~/bin/mirror-hg http://k0s.org/hg

