#!/usr/bin/env bash

# Alternative to silvermirror + unison

set -euxo pipefail

# https://stackoverflow.com/questions/1602324/how-do-i-synchronize-in-both-directions
# https://www.digitalocean.com/community/tutorials/how-to-use-rsync-to-sync-local-and-remote-directories

# TODO: loop over directories?
SRC="${HOME}/docs"

# TODO?: add -zP flags; from
# https://www.digitalocean.com/community/tutorials/how-to-use-rsync-to-sync-local-and-remote-directories
# If you’re transferring files that have not already been compressed, like text files, you can reduce the network transfer by adding compression with the -z option:
# The -P flag is also helpful. It combines the flags --progress and --partial. This first flag provides a progress bar for the transfers, and the second flag allows you to resume interrupted transfers:

mkdir -p "${SRC}"
rsync -au k0s.org:"${SRC}"/ "${SRC}"
rsync -au "${SRC}"/ k0s.org:"${SRC}"
