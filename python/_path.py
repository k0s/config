#!/usr/bin/env python

"""
(filesystem) path utilities

from http://stackoverflow.com/questions/12041525/a-system-independent-way-using-python-to-get-the-root-directory-drive-on-which-p
"""

import os

def is_root(path):
    """is `path` the filesystem root"""
    return not os.path.split(path)[1]

def root(path):
    """return filesystem root of path"""
    path = os.path.abspath(path)
    while not is_root(path):
        path, tail = os.path.split(path)
    return path

if __name__ == '__main__':
    import sys
    for path in sys.argv[1:]:
        print root(path)
