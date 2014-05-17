#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
view graphviz files

http://www.graphviz.org/
"""

# imports
import argparse
import os
import subprocess
import sys
import tempfile

__all__ = ['main']
string = (str, unicode)

class Parser(argparse.ArgumentParser):
    """CLI option parser"""
    def __init__(self):
        argparse.ArgumentParser.__init__(self, description=__doc__)
        self.add_argument('input',
                          help='graphviz file to view')
        self.add_argument('-o', '--output', dest='output',
                          help="path to save to")
        self.add_argument('-e', '--program', dest='program',
                          default='dot',
                          help="GraphViz program to invoke [DEFAULT: %(default)s]")
        self.add_argument('-v', '--view', dest='viewer', default='feh',
                          help="viewer")


def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line
    parser = Parser()
    options = parser.parse_args(args)

    #
    assert os.path.exists(options.input)
    output = options.output or tempfile.mktemp(suffix='.png')

    command = [options.program,
               options.input,
               '-Tpng',
               '-o', output]
    subprocess.check_call(command)
    assert os.path.exists(output)

    if options.viewer:
        subprocess.call([options.viewer, output])

    if not options.output:
        os.remove(output)


if __name__ == '__main__':
  main()

