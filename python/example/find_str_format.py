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
        except KeyError as e:
            retval.add(e.message)


def main(args=sys.argv[1:]):

    string = ' '.join(args)
    keys = find_keys(string)
    print ('\n'.join(sorted(keys)))

if __name__ == '__main__':
    main()
