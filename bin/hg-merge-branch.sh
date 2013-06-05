#!/bin/bash

# merge a hg branch repo
# from https://wiki.mozilla.org/User:Asasaki:Cedar
# TODO: inclusion in mercurial utilities package

if [[ "$#" != "3" ]]
then
    echo "Usage: hg-merge-branch.sh scheme://hg/repository"
    exit 1
fi

if ! hg root
then
    exit 255
fi

# Update to latest
# the hg up -C will blow away any local changes!
#hg pull
#hg up -C -r default

# Pull latest branch changes in
#hg pull $1
#hg merge
#hg commit -m "Merge m-c -> cedar"
