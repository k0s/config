#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tree in python
"""

import optparse
import os
import sys

# ASCII delimeters
ascii_delimeters = {
    'vertical_line' : '|',
    'item_marker'   : '+',
    'last_child'    : '\\'
    }

# unicode delimiters
unicode_delimeters = {
    'vertical_line' : '│',
    'item_marker'   : '├',
    'last_child'    : '└'
    }

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

def tree(directory,
         item_marker=unicode_delimeters['item_marker'],
         vertical_line=unicode_delimeters['vertical_line'],
         last_child=unicode_delimeters['last_child'],
         sort_key=lambda x: x.lower()):
    """
    display tree directory structure for `directory`
    """

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

        files_end =  item_marker
        dirpath_marker = item_marker

        if level > len(indent):
            indent.append(vertical_line)
        indent = indent[:level]

        if dirnames:
            files_end = item_marker
            last[abspath] = dirnames[-1]
        else:
            files_end = last_child

        if last.get(parent) == os.path.basename(abspath):
            # last directory of parent
            dirpath_mark = last_child
            indent[-1] = ' '
        elif not indent:
            dirpath_mark = ''
        else:
            dirpath_mark = item_marker

        # append the directory and piece of tree structure
        # if the top-level entry directory, print as passed
        retval.append('%s%s%s'% (''.join(indent[:-1]),
                                 dirpath_mark,
                                 basename if retval else directory))
        # add the files
        if filenames:
            last_file = filenames[-1]
            retval.extend([('%s%s%s' % (''.join(indent),
                                        files_end if filename == last_file else item_marker,
                                        filename))
                                        for index, filename in enumerate(filenames)])

    return '\n'.join(retval)

def main(args=sys.argv[1:]):

    # parse command line options
    usage = '%prog [options]'
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    parser.add_option('-a', '--ascii', dest='use_ascii',
                      action='store_true', default=False,
                      help="use ascii delimeters (%s)" % ascii_delimeters)
    options, args = parser.parse_args(args)
    if not args:
        args = ['.']

    # sanity check
    not_directory = [arg for arg in args
                     if not os.path.isdir(arg)]
    if not_directory:
        parser.error("Not a directory: %s" % (', '.join(not_directory)))

    delimeters = unicode_delimeters
    if options.use_ascii:
        delimeters = ascii_delimeters

    # print the tree
    for arg in args:
        print (tree(arg, **delimeters))

if __name__ == '__main__':
    main()
