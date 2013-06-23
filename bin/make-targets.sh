#!/bin/bash
# list makefile targets
make -pn | grep '^ *[^#].*:.*' | sed 's/\([^:]+\):.*/\1/' | sort | uniq