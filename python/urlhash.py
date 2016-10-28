#!/usr/bin/env python

"""
return a random URL hash
"""

import random
import urllib

chars = [ chr(i) for i in range(0,255) ]
allowed = [ urllib.quote_plus(i) for i in chars
            if urllib.quote_plus(i) in chars ]

def urlhash(len=10):
  chars = random.sample(allowed, len)
  string = ''.join(chars)
  return urllib.quote_plus(string)

if __name__ == '__main__':
  print urlhash()
