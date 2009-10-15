#!/usr/bin/env python

import sys
import cgi

print cgi.escape(sys.stdin.read())

