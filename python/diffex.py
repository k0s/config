#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
diff before v after of executables (requires http://k0s.org/hg/config/file/f71f6ffa731a/python/lsex.py)
"""

import difflib
import lsex
import optparse
import os
import subprocess
import sys

def add_options(parser):
    """add options to the OptionParser instance"""

def main(args=sys.argv[1:]):

    # parse command line options
    usage = '%prog [options] ...'
    class PlainDescriptionFormatter(optparse.IndentedHelpFormatter):
        """description formatter for console script entry point"""
        def format_description(self, description):
            if description:
                return description.strip() + '\n'
            else:
                return ''
    parser = optparse.OptionParser(usage=usage, description=__doc__, formatter=PlainDescriptionFormatter())
    options, args = parser.parse_args(args)

    # STUB
    # before = lsex... # get executables before
    # raw_input("Press [Enter] to continue")
    # after = lsex... # get executables after
    # difflib.diff() # get difference

if __name__ == '__main__':
  main()

