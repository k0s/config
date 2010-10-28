#!/bin/bash

cd /home/jhammel/mozilla/vpn/Office-vpn/
sudo openvpn --daemon --config Mozilla-MV-Office.ovpn --script-security 3
tail -f /var/log/syslog