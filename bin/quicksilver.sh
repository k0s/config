#!/usr/bin/env bash

# Alternative to silvermirror + unison

set -euxo pipefail

# https://stackoverflow.com/questions/1602324/how-do-i-synchronize-in-both-directions
# https://www.digitalocean.com/community/tutorials/how-to-use-rsync-to-sync-local-and-remote-directories

SRC="${HOME}/docs"

mkdir -p "${SRC}"
rsync -au k0s.org:"${SRC}"/ "${SRC}"
rsync -au "${SRC}"/ k0s.org:"${SRC}"
