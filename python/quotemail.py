#!/usr/bin/env python

"""
quote as per email
"""

def prefix(text, quote='> '):
    return '\n'.join(['%s%s' % (quote, line.rstrip())
                      for line in text.strip().splitlines()])

if __name__ == '__main__':
    import sys
    print prefix(sys.stdin.read())
