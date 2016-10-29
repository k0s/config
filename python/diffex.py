#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
diff before v after of executables
(requires http://k0s.org/hg/config/file/f71f6ffa731a/python/lsex.py)
"""

# improts
import difflib
import lsex
import optparse
import os
import subprocess
import sys
import tempfile


def add_options(parser):
    """add options to the OptionParser instance"""


def main(args=sys.argv[1:]):

    # parse command line
    usage = '%prog [options] ...'
    class PlainDescriptionFormatter(optparse.IndentedHelpFormatter):
        """description formatter for console script entry point"""
        def format_description(self, description):
            if description:
                return description.strip() + '\n'
            else:
                return ''
    parser = optparse.OptionParser(usage=usage,
                                   description=__doc__,
                                   formatter=PlainDescriptionFormatter())
    options, args = parser.parse_args(args)

    # get difference in executables
    before = lsex.executable_names() # get executables before
    raw_input("Press [Enter] to continue")
    after = lsex.executable_names()  # get executables after

    # display
    added = [i for i in after if i not in before]
    removed = [i for i in before if i not in after]
    added.sort()
    removed.sort()

    display = [('Added', added),
               ('Removed', removed),
               ]

    for display_name, var in display:
        if var:
            print '%s:' % display_name
            print ('\n'.join(var))


if __name__ == '__main__':
  main()

