#!/usr/bin/env python

import os
import random
import subprocess
import sys

from optparse import OptionParser

"""randomize a bunch of files"""

if __name__ == '__main__':
    usage = '%prog [options] file_or_directory <...>'
    parser = OptionParser(usage=usage, description=__doc__)
    parser.add_option("-e", "--exec", dest="callable",
                      help="program to execute for each file")
    options, argv = parser.parse_args()
    if not argv:
        argv = ['.']
    args = []
    for i in argv:
        if os.path.isdir(i):
            for root, dirs, files in os.walk(i):
                args.extend([os.path.join(root, f) for f in files])
        else:
            args.append(i)
    random.shuffle(args)
    if options.callable:
        for i in args:
            subprocess.call([options.callable, i])
    else:
        print '\n'.join(args)
