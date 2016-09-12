#!/bin/bash
export BRANCH=$(git branch | grep \* | cut -d ' ' -f2)
export PATCH=$(mktemp --suffix .diff)
echo Patch at $PATCH
git diff $(git merge-base HEAD master) > ${PATCH}
cd `git rev-parse --show-toplevel`
patch -p1 < ${PATCH}
