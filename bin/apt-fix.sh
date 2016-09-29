#!/bin/bash
# from http://askubuntu.com/questions/263378/how-to-fix-dependencies-broken-packages
sudo sh -c "apt-get update;apt-get dist-upgrade;apt-get autoremove;apt-get autoclean"
