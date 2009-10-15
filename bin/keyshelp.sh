#!/bin/bash

# help message for fluxbox keys
if which gxmessage
then
    XMESSAGE="gxmessage -borderless"
else
    XMESSAGE=xmessage
fi

cat <(echo -e "Press <Control>+<Alt>+key to use the commands: \n") <(sed -n '/Control Mod1.*ExecCommand/ {s/Control Mod1//g;s/ExecCommand//g;s/:.*#/:/g;p}' ~/.fluxbox/keys) | ${XMESSAGE} -timeout 20 -nearmouse -file -
