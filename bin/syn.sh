#!/bin/bash

set -ex

cd

~/k0s/bin/silvermirror
hg pull

set +e
hg push  # will exit 1 on no changes found
set -e

ubuntu_updated.sh
~/k0s/bin/mirror-hg http://k0s.org/hg

