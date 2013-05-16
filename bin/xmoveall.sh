#!/bin/bash

# move all windows to a desktop
# by default, the final one (graveyard)

# List  all  desktops  managed  by the window manager. One line is
# output for each desktop, with the line broken up into space sepâ
# arated  columns.  The  first  column contains an integer desktop
# number. The second column contains a '*' character for the  curâ
# rent  desktop,  otherwise  it contains a '-' character. The next
# two columns contain the fixed string DG: and  then  the  desktop
# geometry as '<width>x<height>' (e.g. '1280x1024'). The following
# two columns contain the fixed string VP: and then  the  viewport
# position  in  the  format '<y>,<y>' (e.g. '0,0'). The next three
# columns after this contains the fixed string WA:  and  then  two
# columns  with  the workarea geometry as 'X,Y and WxH' (e.g. '0,0
# 1280x998'). The rest of the line contains the name of the  desktop
# (possibly containing multiple spaces).
DESKTOP=$(wmctrl -d | awk '{if ($2 == "*") {print $1}}')

# find the last desktop
if (( $# ))
then
LAST=$1
else
LAST=$(wmctrl -d | tail -n 1 | awk '{print $1}')
fi

#  -l     List the windows being managed by the window manager.
wmctrl -l | awk '{if ($2 == "'${DESKTOP}'") {print $1}}' | while read line
do
# -t <DESK>
# Move  a window that has been specified with the -r action to the
# desktop <DESK>.
wmctrl -i -r ${line} -t ${LAST}
done

