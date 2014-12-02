#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
find str format options
"""

import argparse
import os
import subprocess
import sys

__all__ = ['main']

def find_keys(string):
    retval = set()
    while True:
        try:
            string.format(**{i:'' for i in retval})
            return retval
        except KeyError:
            import pdb; pdb.set_trace()

def main(args=sys.argv[1:]):

    # parse command line
    string = ' '.join(args)

if __name__ == '__main__':
    main()
