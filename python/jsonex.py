#!/usr/bin/env python

"""
JSON explorer
"""

import argparse
import json
import os
import sys
import urllib2

def dereference(obj, key):
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj[key]
    return obj[int(key)]

def main(args=sys.argv[1:]):

    # command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?',
                        help="input file or url (read from stdin if ommitted)")
    parser.add_argument('object', nargs='*',
                        help="object in dotted notation")

    options = parser.parse_args(args)

    # get data
    if not options.input or options.input == '-':
        data = sys.stdin
    elif'://' in options.input:
        data = urllib2.urlopen(options.input)
    else:
        data = open(options.input, 'r')
    obj = json.load(data)

    if options.object:
        for o in options.object:
            base = obj
            for key in o.strip().split('.'): # split into objects
                base = dereference(base, key)
                if base is None:
                   break
            print (json.dumps(base))
    else:
        print (json.dumps(obj, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
