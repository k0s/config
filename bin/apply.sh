#!/bin/bash
# apply a patch from the web
# TODO: take from file as well

LVL=1
if ((curl $1 2> /dev/null) | (patch -p${LVL} --dry-run -b > /dev/null))
then
  echo "hi"
fi
