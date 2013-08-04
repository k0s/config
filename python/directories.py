#!/usr/bin/env python

"""
ls unique file paths
"""

import optparse
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))

def main(args=sys.argv[1:]):

    usage = '%prog [options]'
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    parser.add_option('--strip', default='? ')
    options, args = parser.parse_args(args)

    _input = sys.stdin.read()
    lines = [i.strip() for i in _input.splitlines()
             if i.strip()]
    lines = [i[len(options.strip):] if i.startswith(options.strip) else i
             for i in lines]
    paths = set([i.split(os.path.sep)[0] for i in lines])
    for i in sorted(paths):
        print i

if __name__ == '__main__':
    main()
