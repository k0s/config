#!/usr/bin/env python

"""
quote text
"""

# TODO:
# - combine with quotemail...wth?
# -> textshaper

import sys
import textwrap
from subprocess import check_output as call

def quote(text, prefix='> ', width=69):
    """
    returns quoted text
    - prefix: string to prepend quote
    - width: final width (emacs wraps at 70)
    """
    width -= len(prefix) # subtract the prefix
    text = text.strip() # remove surrounding whitespace
    lines = []
    for line in text.splitlines():
        line = line.strip()
        lines.extend(textwrap.wrap(line, width))
    return '\n'.join(['%s%s' % (prefix, line)
                      for line in lines])

def main(args=sys.argv[1:]):
    text = sys.stdin.read()
    sys.stdout.write(quote(text))

if __name__ == '__main__':
    main()
