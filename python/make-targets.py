#!/usr/bin/python

"""
list the targets for a makefile
"""

import argparse
import subprocess
import sys

call = subprocess.check_output

def main(args=sys.argv[1:]):

    ignore = ['%', '.', '(', '/']

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all", action="store_true",
                        help="show all matches")
    parser.add_argument("--origin", action="store_true",
                        help="show original line")
    args = parser.parse_args(args)

    if args.all:
        ignore = []

    line_dict = {}
    names = []
    output = call(["make", "-pn"]).strip()
    for index, line in enumerate(output.splitlines()):
        _orig = line
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        if ':' not in line:
            continue
        name, rhs = line.split(':', 1)
        if rhs and rhs[0] == '=':
            continue
        name = name.strip()
        if '=' in name or not name:
            continue

        # ignore thingies
        if name.startswith(tuple(ignore)):
            continue

        names.append(name)
        line_dict.setdefault(name, (index, _orig))

    names = list(set(names))
    names.sort()
    if args.origin:
        for name in names:
            index, line = line_dict[name]
            print '%s: `%s`:%d' % (name, line, index+1)
        return
    print '\n'.join(names)

if __name__ == '__main__':
    main()
