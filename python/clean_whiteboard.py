#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
From https://gist.github.com/lelandbatey/8677901

#!/bin/bash
convert $1 -morphology Convolve DoG:15,100,0 -negate -normalize -blur 0x1 -channel RBG -level 60%,91%,0.1 $2
"""

import argparse
import os
import subprocess
import sys

__all__ = ['main']
here = os.path.dirname(os.path.realpath(__file__))
string = (str, unicode)

def main(args=sys.argv[1:]):

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',
                        help='input file')
    parser.add_argument('output',
                        help='output file')
    options = parser.parse_args(args)

    subprocess.check_call(['convert', options.input, '-morphology', 'Convolve', 'DoG:15,100,0', '-negate', '-normalize', '-blur', '0x1', '-channel', 'RBG', '-level', '60%,91%,0.1', options.output])

if __name__ == '__main__':
    main()
