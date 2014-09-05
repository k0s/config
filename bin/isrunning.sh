#!/bin/bash

# are the given processes running?

for i in "$@";
do
    ps axwww | grep --colour=auto "$i" | grep --colour=auto -v 'grep';
done | sort | uniq
