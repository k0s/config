#!/usr/bin/env python

"""
Top-Level Domain names (TLDs), country codes only
"""

import argparse
import sys
import urllib2

URL = 'http://www.palosverdes.com/jesse/irc/country.txt'


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

def main(args=sys.argv[1:]):
  """CLI"""

  # parse command line
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('tld', nargs='+',
                      help="country-code TLD to look up")
  options = parser.parse_args(args)

  # lookup + output
  for arg in options.tld:
    print ('{}: {}'.format(arg, get(arg)))

if __name__ == '__main__':
  main()
