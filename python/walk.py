#!/usr/bin/env python

"""
illustration of walking a directory structure
"""

# imports
import argparse
import os
import sys


def ensure_dir(path):
    """ensures `path` is a directory"""
    return os.path.isdir(path)


def all_files(directory):
    filenames = []
    for dirpath, dirnames, files in os.walk('/home/jhammel/music'):
        filenames.extend([os.path.join(dirpath, f) for f in files])
    return sorted(filenames)


def main(args=sys.argv[1:]):
    """CLI"""


    # parse command line

    # sanity
    if not args:
        print "Usage: %s directory [directory] [...]" % os.path.basename(sys.argv[0])

    # process command line
    for arg in args:
        if os.path.isdir(arg):
            for i in all_files(arg):
                print i
        elif os.path.isfile(arg):
            print os.path.abspath(arg)
        else:
            sys.stderr.write("'%s' not a file or directory\n" % arg)


if __name__ == '__main__':
    main()
