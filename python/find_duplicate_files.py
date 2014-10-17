#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
find duplicate files in a directory
"""

# imports
import argparse
import os
import subprocess
import sys

# module globals
__all__ = ['main', 'Parser']

class Parser(argparse.ArgumentParser):
    """CLI option parser"""
    def __init__(self, **kwargs):
        kwargs.setdefault('description', __doc__)
        argparse.ArgumentParser.__init__(self, **kwargs)
        self.add_argument('directory')
        self.options = None

    def parse_args(self, *args, **kw):
        options = argparse.ArgumentParser.parse_args(self, *args, **kw)
        self.validate(options)
        self.options = options
        return options

    def validate(self, options):
        """validate options"""
        if not os.path.isdir(options.directory):
            self.error("Not a directory: {}".format(options.directory))

def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line options
    parser = Parser()
    options = parser.parse_args(args)

    output = subprocess.check_output(['ls', '-l', options.directory]).strip()
    rows = [row.strip().split() for row in output.splitlines()[1:]]

    sizes = {}
    for row in rows:
        size = int(row[4])
        filename = row[-1]
        sizes.setdefault(size, []).append(filename)

    duplicates = {}
    for size, filenames in sizes.items():
        if len(filenames) < 2:
            continue
        duplicates[size] = filenames

    for size in sorted(duplicates.keys()):
        print ('{} : '.format(size))
        print ('\n'.join(duplicates[size]))
        print ('\n')

if __name__ == '__main__':
    main()
