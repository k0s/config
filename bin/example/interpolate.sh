#!/bin/bash

if [ "$#" == "0" ]
then
    echo "Usage: $0 file [file] [...]"
    exit 1
fi

for arg in "$@"
do
    eval "cat <<EOF
$(<$arg)
EOF
" 2> /dev/null
done