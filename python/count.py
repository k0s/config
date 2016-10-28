#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
counting and duplication
"""

# imports
import argparse
import sys
from collections import OrderedDict

# module globals
__all__ = ['main', 'CountParser']


def count(*items):
    """count the occurance of each (hashable) item"""
    counts = OrderedDict()
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts

def duplicates(*items):
    """returns set of duplicate items"""
    return set([key for key, value in count(*items).items()
                if value > 1])

class CountParser(argparse.ArgumentParser):
    """CLI option parser"""

    def __init__(self, **kwargs):
        kwargs.setdefault('formatter_class', argparse.RawTextHelpFormatter)
        kwargs.setdefault('description', __doc__)
        argparse.ArgumentParser.__init__(self, **kwargs)
        self.add_argument('input', nargs='?',
                          type=argparse.FileType('r'), default=sys.stdin,
                          help="file to read items from, or stdin by default")
        self.add_argument('--duplicates', dest='duplicates',
                          action='store_true', default=False,
                          help="print (sorted) duplicates, not counts")
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
    parser = CountParser()
    options = parser.parse_args(args)

    # read a thing
    try:
        items = options.input.read().strip().split()
    except KeyboardInterrupt:
        # probably trying to read stdin interactively
        # revert! revert! revert!
        return

    if options.duplicates:
        print ('\n'.join(sorted(duplicates(*items))))
    else:
        # get the counts
        for key, value in count(*items).items():
            print ('{}:{}'.format(key, value))

if __name__ == '__main__':
    main()
