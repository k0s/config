#!/usr/bin/env python

import os
import sys

def all_files(directory):
    filenames = []
    for dirpath, dirnames, files in os.walk('/home/jhammel/music'):
        filenames.extend([os.path.join(dirpath, f) for f in files])
    return sorted(filenames)

def main(args=sys.argv[1:]):
    if not args:
        print "Usage: %s directory [directory] [...]" % os.path.basename(sys.argv[0])
    for arg in args:
        if os.path.isdir(arg):
            for i in all_files(arg):
                print i
        elif os.path.isfile(arg):
            print os.path.abspath(arg)
        else:
            print >> sys.stderr, "'%s' not a file or directory"
        
if __name__ == '__main__':
    main()
