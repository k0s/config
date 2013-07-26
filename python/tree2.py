#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tree in python
"""

import optparse
import os
import sys

# ASCII delimeters
VERTICAL_LINE = '|'
ITEM = '+'
END = '\\'

# unicode delimiters
VERTICAL_LINE = '│'
ITEM = '├'
END  = '└'

def depth(directory):
    """returns the integer depth of a directory or path relative to '/' """

    directory = os.path.abspath(directory)
    level = 0
    while True:
        directory, remainder = os.path.split(directory)
        level += 1
        if not remainder:
            break
    return level

def tree(directory, sort_key=lambda x: x.lower()):

    retval = []
    indent = []
    last = {}
    top = depth(directory)

    for dirpath, dirnames, filenames in os.walk(directory, topdown=True):

        abspath = os.path.abspath(dirpath)
        basename = os.path.basename(abspath)
        parent = os.path.dirname(abspath)
        level = depth(abspath) - top

        # sort articles of interest
        for resource in (dirnames, filenames):
            resource[:] = sorted(resource, key=sort_key)

        files_end =  ITEM
        dirpath_marker = ITEM

        if level > len(indent):
            indent.append(VERTICAL_LINE)
        indent = indent[:level]

        if dirnames:
            files_end = ITEM
            last[abspath] = dirnames[-1]
        else:
            files_end = END

        if last.get(parent) == os.path.basename(abspath):
            # last directory of parent
            dirpath_mark = END
            indent[-1] = ' '
        elif not indent:
            dirpath_mark = ''
        else:
            dirpath_mark = ITEM

        retval.append('%s%s%s'% (''.join(indent[:-1]), dirpath_mark, basename))
        if filenames:
            last_file = filenames[-1]
            retval.extend([('%s%s%s' % (''.join(indent),
                                        files_end if filename == last_file else ITEM,
                                        filename))
                                        for index, filename in enumerate(filenames)])

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
