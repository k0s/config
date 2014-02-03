#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
from subprocess import check_output

def call(command, **kwargs):
    kwargs.setdefault('shell', True)
    print (command)
    return check_output(command, **kwargs)

def main(args=sys.argv[1:]):

    usage = '%prog [options]'
    parser = argparse.ArgumentParser(usage=usage, description=__doc__)
    parser.add_argument('--mark', dest='mark', default='#')
    parser.add_argument('-d', '--directory', dest='directory', default='.')
    parser.add_argument('-p', '--pattern', dest='pattern', default='*.py')
    options = parser.parse_args(args)

    command = ['find', options.directory, '-iname', options.pattern,
               '|',
               'grep', '' ... ] # to finish

    output = check_output(subprocess.list2cmdline(command))

if __name__ == '__main__':
    main()
