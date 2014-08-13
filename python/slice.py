#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
slice a arbitrarily sized list
"""

# imports
import argparse
import os
import subprocess
import sys

# module globals
__all__ = ['slice', 'main', 'Parser']

def slice(container, n_chunks):
    size = int(len(container)/(n_chunks-1))
    retval = []
    start = 0
    for i in range(n_chunks-1):
        retval.append(container[start:start+size])
        start += size
    retval.append(container[start:])
    return retval

class Parser(argparse.ArgumentParser):
    """CLI option parser"""
    def __init__(self, **kwargs):
        kwargs.setdefault('description', __doc__)
        argparse.ArgumentParser.__init__(self, **kwargs)
        self.add_argument('N', type=int,
                          help="number of chunks")
        self.add_argument('-M', '--len', dest='length', type=int, default=29,
                          help="length of list [DEFAULT: %(default)s]")
        self.options = None

    def parse_args(self, *args, **kw):
        options = argparse.ArgumentParser.parse_args(self, *args, **kw)
        self.validate(options)
        self.options = options
        return options

    def validate(self, options):
        """validate options"""

def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line options
    parser = Parser()
    options = parser.parse_args(args)

    # generate list
    seq = range(options.length)

    # chunk list
    output = slice(seq, options.N)

    # print output
    for chunk in output:
        print (",".join([str(i) for i in chunk]))

if __name__ == '__main__':
    main()

