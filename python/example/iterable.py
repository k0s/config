#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
illustration of a class iterable
"""
# XXX does not work!!@ TODO!!! XXX #

import argparse
import sys

class MyIterable(object):
    def __init__(self, max):
        self.items = list(range(max))
    def __iter__(self):
        return self
    def next(self):
        for i in self.items:
            yield i

def main(args=sys.argv[1:]):

    usage = '%prog [options]'
    parser = argparse.ArgumentParser(usage=usage, description=__doc__)
    options = parser.parse_args(args)

    myiter = MyIterable(10)
    for i in myiter:
        print ('Hi {}'.format(i))

if __name__ == '__main__':
    main()
