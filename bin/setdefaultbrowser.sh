#!/bin/bash

# To get all selections:
# update-alternatives --get-selections

# To get a particular selection:
# update-alternatives --display x-www-browser

# http://askubuntu.com/questions/100693/how-can-i-manually-change-the-default-web-browser
# http://askubuntu.com/questions/45885/how-do-i-set-a-custom-browser-as-default-in-preferred-applications?rq=1
# http://fvue.nl/wiki/Linux:_Default_browser

# cat /proc/$(pidof krunner)/environ | tr '\000' '\012' | grep BROWSER

if [[ $(whoami) != 'root' ]]
then
   echo "Must be run as root"
   exit 1
fi

BROWSER=/home/jhammel/firefox/firefox
PREFIX=/usr/bin
for LINK in gnome-www-browser x-www-browser
do
    LINKPATH=${PREFIX}/${LINK}
    update-alternatives --install ${LINKPATH} ${LINK} ${BROWSER} 99
    update-alternatives --install ${LINKPATH} ${LINK} ${BROWSER} 99
    update-alternatives --set ${LINK} ${BROWSER}
    update-alternatives --display ${LINK}
#    unlink ${LINKPATH}
#    ln -s  ${BROWSER} ${LINKPATH}
done
