#!/bin/bash

INTERFACE=eth0

ifconfig ${INTERFACE} | grep 'HWaddr' | sed 's/.*HWaddr \(.*\) /\1/'