#!/bin/bash

set -e

cd

silvermirror
hg sync
ubuntu_updated.sh
~/bin/mirror-hg http://k0s.org/hg

