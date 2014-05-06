#!/bin/bash

PID=$$

echo "The PID of this shell script is ${PID}"
ps auxwww | grep ${PID}
kill ${PID}