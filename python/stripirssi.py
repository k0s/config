#!/usr/bin/env python

import optparse
import os
import sys

"""
strip irssi comments and format
"""

# TODO : -> textshaper

### generic functionality

string = (basestring,)

class splitlines(object):
    def __init__(self, function):
        self.function = function
    def __call__(self, lines, *args, **kwargs):
        if isinstance(lines, string):
            lines = lines.strip().splitlines()
        self.function(lines, *args, **kwargs)

@splitlines
def strip(lines):
    return [line.strip() for line in lines]

@splitlines
def strip_first_column(lines, separator=None):
    """
    removes leading column (defined by separator) from lines of text
    """
    # TODO: -> genericize
    # - and handle whitespace more generically

    length = None # length of first column
    stripped = []
    for line in lines:
        if not line:
            continue # XXX desirable?
        prefix, rest = line.split(separator, 1)
        if length is not None:
            length = len(prefix)
        else:
            if len(prefix) != length:
                if not line[:len(prefix)].isspace():
                    raise AssertionError # XXX
        stripped.append(line[length:])
    return stripped

@splitlines
def remove_lines(lines, startswith):
    return [line for line in lines
            if line.startswith(startswith)]
    # really, one could take most functions for str and map -> lines

@splitlines
def remove_time(lines):
    """removes leading 24 hour timestamp: HH:MM"""
    # XXX :ss?

@splitlines
def join(lines):
    """DOCUMENT ME!"""
    last = None
    joined = []
    for line in lines:
        if line:
            if line[0].isspace():
                line = line.strip()
                if not line:
                    if last:
                        joined.append(last)
                    continue
                if last:
                    last = '%s %s' % (last, line.strip())
                else:
                    joined.append(line.strip()
            else:
                if last:
                    joined.append(last)
                    last = line.rstrip()
        else:
            if last:
                joined.append(last)
    return joined

### CLI

def main(args=sys.argv[1:]):

    usage = '%prog [options]'
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    parser.add_option('-i', '--in-place', dest='in_place',
                      help="rewrite files in place")
    #    parser.add_option - strip timestamps only
    #    parser.add_option - strip nicks
    options, args = parser.parse_args(args)

if __name__ == '__main__':
    main()
