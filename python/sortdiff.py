#!/usr/bin/env python

import optparse
import os
import sys

def main(args=sys.argv[1:]):

    usage = '%prog [options]'
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    options, args = parser.parse_args(args)

    lines = sys.stdin.readlines()
    diff = {'+': set(),
            '-': set()}
    for line in lines:
        for key, value in diff.items():
            if line.startswith(key):
                value.add(line[1:].strip())

    added = diff['+'].difference(diff['-'])
    minus = diff['-'].difference(diff['+'])

    print '+++'
    for line in sorted(added):
        print line
    print '---'
    for line in sorted(minus):
        print line

if __name__ == '__main__':
    main()
