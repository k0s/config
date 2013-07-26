#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tree in python
"""

import optparse
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))

def depth(directory):
    directory = os.path.abspath(directory)
    level = 0
    while True:
        directory, remainder = os.path.split(directory)
        level += 1
        if not remainder:
            break
    return level

def tree(directory):
    retval = []
    level = depth(directory)
    pre = []
    directories = {}
    lvlndctr = []
    last = {}
    passed_last = {}
    columns = []
    lastdepth = depth
    indent = 0
    for dirpath, dirnames, filenames in os.walk(directory, topdown=True):
        basename = os.path.basename(dirpath)
        parent = os.path.abspath(os.path.dirname(dirpath))
        indent = depth(dirpath) - level
        dirnames[:] = sorted(dirnames, key=lambda x: x.lower())
        last[os.path.abspath(dirpath)] = dirnames and dirnames[-1] or None
        directories[dirpath] = dirnames

        retval.append('%s%s%s' % ('│' * (indent-1),
                                     ('├' if basename == basename else '└') if indent else '',
                                     basename))
        filenames = sorted(filenames, key=lambda x: x.lower())
        retval.extend(['%s%s%s' % ('│' * (indent),
                                   '├' if (((index < len(filenames) -1)) or dirnames) else '└',
                                    name)
                       for index, name in
                       enumerate(filenames)
                       ])
    return '\n'.join(retval)

def main(args=sys.argv[1:]):

    usage = '%prog [options]'
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    options, args = parser.parse_args(args)
    if not args:
        args = ['.']

    not_directory = [arg for arg in args
                     if not os.path.isdir(arg)]
    if not_directory:
        parser.error("Not a directory: %s" % (', '.join(not_directory)))

    for arg in args:
        print (tree(arg))

if __name__ == '__main__':
    main()
