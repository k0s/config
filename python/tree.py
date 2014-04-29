#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tree in python
"""

# TODO: script2package

import argparse
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


### stuff for tree generalization

class Tree(object):
    """tree structure in python"""

    def __init__(self, parent=None):
        self.parent = parent
        self._children = []

    def children(self):
        """returns children of the tree"""
        return self._children # base implementation

    def add(self, item):
        """add a child to the tree root"""

    def update(self, tree):
        """add a subtree to the tree"""
        self.add(tree)
        tree.parent = self # XXX .add should probably do this for scary reasons

    def output(self, serializer):
        """output the tree via the given serializer"""
        # XXX or should this method exist at all and instead the
        # __call__ method of serializers take a Tree object?

class DirectoryTree(Tree):
    """directory structure as a tree"""

    def __init__(self, directory):
        self.directory = directory
        self._return_type = os.path.abspath

    def children(self):
        return os.listdir(self.directory) # -> self._return_type

## Serializers

def tree2html(tree):
    """
    .
    ├── a8e.py
    ├── abstract.py
    ├── accentuate.py

    ->

    <ul>
    <li>a8e.py</li>
    ...
    """


# How to serialize a tree -> JSON?

###

def tree(directory,
         item_marker=unicode_delimeters['item_marker'],
         vertical_line=unicode_delimeters['vertical_line'],
         last_child=unicode_delimeters['last_child'],
         display_files=True,
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

        # omit files if specified
        if not display_files:
            filenames = []

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
    """CLI"""

    # parse command line options
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-a', '--ascii', dest='use_ascii',
                        action='store_true', default=False,
                        help="use ascii delimeters ({})".format(', '.join(ascii_delimeters.values())))
    parser.add_argument('-d', '--no-files', dest='display_files',
                        action='store_false', default=True,
                        help='only display directories')
    parser.add_argument('path', nargs='*',
                        help="directory paths to display the tree of")
    options = parser.parse_args(args)

    # get paths to operate on
    paths = options.path
    if not paths:
        paths = ['.']

    # ensure each path is a directory
    not_directory = [arg for arg in paths
                     if not os.path.isdir(arg)]
    if not_directory:
        parser.error("Not a directory: {}".format(', '.join(not_directory)))

    delimeters = unicode_delimeters
    if options.use_ascii:
        delimeters = ascii_delimeters

    # build function arguments
    kw = delimeters.copy()
    kw['display_files'] = options.display_files

    # print the tree
    for arg in paths:
        print (tree(arg, **kw))

if __name__ == '__main__':
    main()
