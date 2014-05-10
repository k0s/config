#!/bin/bash
# -*- coding: utf-8 -*-

# really remove Ubuntu packages
# http://www.piprime.fr/1480/manually-remove-broken-package-debian-ubuntu/

for PACKAGE in $@
do
  echo "Removing ${PACKAGE}"
  sudo mv /var/lib/dpkg/info/${PACKAGE}.* /tmp/
  sudo dpkg --remove --force-remove-reinstreq ${PACKAGE}
done
