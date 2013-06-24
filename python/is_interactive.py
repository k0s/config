#!/usr/bin/env python

"""
illustrates usage of isatty

Ref: http://www.tutorialspoint.com/python/file_isatty.htm
"""

import optparse
import os
import sys

# DOES NOT WORK! :(
# > echo 'foo' | is_interactive.py
# Usage: is_interactive.py [options]

# is_interactive.py: error: missing input


def main(args=sys.argv[1:]):
    parser = optparse.OptionParser()
    options, args = parser.parse_args(args)

    function = str.upper

    if args:
        # take input from command line args
        input = ' '.join(args)
    elif not sys.stderr.isatty():
        # take input from stdin
        input = sys.stdin.read()
    else:
        # no input! cry!
        parser.error("missing input")

    print function(input)

if __name__ == '__main__':
    main()
