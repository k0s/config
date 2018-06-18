#!/usr/bin/env python

import os
import sys
from optparse import OptionParser

try:
    # python 2
    string = (str, unicode)
except NameError:
    # python 3
    string = (str,)

def ordered_set(alist):
    """make sure duplicate path elements aren't printed twice"""

    seen = set()
    new = []
    for item in alist:
        if item in seen:
            continue
        seen.add(item)
        new.append(item)
    return new

def lsex(path=None):
    """
    list of executable files on the path

    - path: list or PATH-style string of directories to search.
            if not specified, use system PATH
    """

    if path is None:
        # use system path
        path = os.environ['PATH']
    if isinstance(path, string):
        path = ordered_set(path.split(os.pathsep))

    executables = []

    # add the executable files to the list
    for i in path:
        if not os.path.isdir(i):
            continue
        files = [ os.path.join(i,j) for j in os.listdir(i) ]
        files = list(filter(lambda x: os.access(x, os.X_OK), files))
        files.sort() # just to make the output pretty
        executables.extend(files)
    return executables

def executable_names(path=None):
    executables = lsex(path)
    executables = set([os.path.basename(i) for i in executables])
    return executables

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--names', action='store_true', default=False,
                      help="list only the set of names")

    options, args = parser.parse_args()
    if options.names:
        print ('\n'.join(sorted(executable_names())))
        sys.exit(0)

    for i in lsex():
        print (i)
