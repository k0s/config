#!/usr/bin/env python

'''

'''

import optparse
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))

def main(args=sys.argv[1:]):

    usage = '%prog [options] repository <repository> <...>'
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    parser.add_option('--ssh', dest='default_push_ssh',
                      action='store_true', default=False,
                      help="")
    options, args = options.parse_args(args)
    if not args:
        parser.print_usage()
        parser.exit()

    # find all .hgrc files
    hgrc = []

    # all the error types
    missing = []
    not_hg = []
    not_a_directory = []

    for path in args:
        if not os.path.exists(path):
            missing.append(path)
        path = os.path.abspath(os.path.normpath(path))
        if os.path.isdir(path):
            basename = os.path.basename(path)
            subhgdir = os.path.join(path, '.hg') # hypothetical .hg subdirectory
            if basename == '.hg':
                hgrcpath = os.path.join(path, 'hgrc')
            elif os.path.exists(subhgdir):
                if not os.path.isdir(subhgdir):
                    not_a_directory.append(subhgdir)
                    continue
            else:
                not_hg.append(path)
                continue



if __name__ == '__main__':
    main()
