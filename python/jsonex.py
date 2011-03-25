#!/usr/bin/env python

"""
JSON explorer
"""

import json
import sys
from pprint import pprint

def main(args=sys.argv[1:]):
    data = sys.stdin.read() # read from stdin
    obj = json.loads(data)

    if args:
        for arg in args:
            foo = arg.split('.') # split into objects
            # TODO: split into slice notation
            pass # TODO
    else:
        print json.dumps(obj, indent=2, sort_keys=True)

if __name__ == '__main__':
    main()
