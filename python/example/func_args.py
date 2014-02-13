#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
get args of your own function

http://stackoverflow.com/questions/582056/getting-list-of-parameter-names-inside-python-function
"""

import argparse
import inspect
import os
import subprocess
import sys

def foo(bar=None, fleem=None, blah=None):
    frame = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(frame)
    print 'function name "%s"' % inspect.getframeinfo(frame)[2]
    for i in args:
        print "    %s = %s" % (i, values[i])
    return [(i, values[i]) for i in args]

def main(args=sys.argv[1:]):

    parser = argparse.ArgumentParser()
    options = parser.parse_args(args)
    foo(1, 2, 3)

if __name__ == '__main__':
    main()
