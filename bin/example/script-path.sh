#!/bin/bash

# echoes path to this script (example)

echo "argv[0]: $0"
path=`readlink -f $0`
echo "path: ${path}"
