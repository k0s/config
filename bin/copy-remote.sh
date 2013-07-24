#!/bin/bash

# TODO -> silvermirror
# (STUB)

REMOTE=k0s.org

if ! echo $PWD | grep '^'$HOME
then
  echo "should be in subtree of $HOME to use"
  exit 1
fi

for i in "$@"
do
  if [ ! -e $i ]
  then
      echo "Error: $i does not exist"
      exit 1
  fi
done

for i in "$@"
do
 path=$(readlink -f $i)
 if [ "${path:0:1}" != "/" ]
 then
 # relative path
 #path=${PWD}/${path}
 fi
 scp ${REMOTE}:${path} ${path}
done