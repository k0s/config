#!/bin/bash

sed -e 's/^ *//g' -e 's/ *$//g' | tr '\n' ' '
echo