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

    # get output name from input
    output_filename = os.path.splitext(os.path.basename(input))[0] + '.html'
    output = os.path.join(os.path.dirname(input), output_filename)

    # build command line
    options = []
    command = ['rst2s5.py']
    command.extend(options)
    command.extend([input, output])
    print subprocess.list2cmdline(command)

    # call it
    subprocess.call(command)

if __name__ == '__main__':
    main()
