#!/bin/bash

# swap screens between internal laptop monitor and external monitor
# XXX sensitive to the individual laptop :(

# See also `unxrandr`:
# unxrandr - inverse tool of xrandr
# unxrandr  is  a  tool  that  queries  the  XRandR  state using ARandR's
# libraries and outputs an xrandr command line that reproduces the  state


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