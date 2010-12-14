#!/usr/bin/env python

URL = 'http://www.palosverdes.com/jesse/irc/country.txt'

import urllib2

def codes():
  f = urllib2.urlopen(URL)
  codes = {}
  for line in f.readlines():
    line = line.strip()
    if not line:
      continue
    key, value = line.split(None, 1)
    codes[key.lower()] = value
  return codes
codes = codes()

def get(code):
  code = code.lstrip('.').lower()
  return codes.get(code)

if __name__ == '__main__':
  import sys
  for arg in sys.argv[1:]:
    print '%s: %s' % (arg, get(arg))
