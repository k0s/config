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


class DuplicateFilesParser(argparse.ArgumentParser):
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
    parser = DuplicateFilesParser()
    options = parser.parse_args(args)

    # get all files
    raise NotImplementedError('TODO') # -> record TODO items

if __name__ == '__main__':
    main()
