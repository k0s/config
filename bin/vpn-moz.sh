#!/bin/bash

cd /home/jhammel/mozilla/vpn/Mozilla-vpn
sudo openvpn --daemon --config MozillaVPN.ovpn --script-security 3
tail -f /var/log/syslog