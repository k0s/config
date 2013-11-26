#!/bin/bash

cd /home/jhammel/mozilla/vpn/Mozilla-vpn
sudo openvpn --daemon --config Mozilla-MPT.ovpn --script-security 3
tail -f /var/log/syslog