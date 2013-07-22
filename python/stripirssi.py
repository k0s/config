#!/usr/bin/env python

import optparse
import os
import sys

"""
strip irssi comments
"""

# XXX stub

here = os.path.dirname(os.path.realpath(__file__))

def main(args=sys.argv[1:]):

    usage = '%prog [options]'
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    parser.add_option('-i', '--in-place', dest='in_place',
                      help="rewrite files in place")
    #    parser.add_option - strip timestamps only
    #    parser.add_option - strip nicks
    options, args = parser.parse_args(args)

if __name__ == '__main__':
    main()
