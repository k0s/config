#!/bin/bash

sudo openvpn --daemon --config /home/jhammel/mozilla/vpn/MPT-vpn/Mozilla-MPT.ovpn --script-security 3
tail -f /var/log/syslog