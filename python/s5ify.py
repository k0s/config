#!/usr/bin/env python

"""
my front end to rst2st.py
"""

# imports
import argparse
import os
import subprocess
import sys

def normalize_filename(filename):
    return None  # TODO

def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    options = parser.parse_args(args)

    # sanity
    input = options.input
    if not os.path.isfile(input):
        parser.error("Not a file: '{}'".format(input))
    input = os.path.abspath(options.input)

if __name__ == '__main__':
    main()
