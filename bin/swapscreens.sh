#!/bin/bash

# swap screens between internal laptop monitor and external monitor

INTERNAL="LVDS1"
EXTERNAL="VGA1"
INTERNAL_MODE="1366x768"
EXTERNAL_MODE="1600x1200"

xwininfo -root | grep "geometry $EXTERNAL_MODE"
if [ $? -eq 0 ]
then
 xrandr --output $EXTERNAL --off --output $INTERNAL --mode $INTERNAL_MODE
else
 xrandr --output $INTERNAL --off --output $EXTERNAL --mode $EXTERNAL_MODE
fi