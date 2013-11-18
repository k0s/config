#!/usr/bin/env python

"""
compare differences of url contents
"""

import difflib
import optparse
import os
import sys
import urllib2

here = os.path.dirname(os.path.realpath(__file__))

def main(args=sys.argv[1:]):

    usage = '%prog [options] from-url to-url'
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    parser.add_option('--bash', '--command', dest='command',
                      action='store_true', default=False,
                      help="prepend output with bash command")
    options, args = parser.parse_args(args)
    if len(args) != 2:
        parser.print_usage()
        parser.exit(1)

    contents = {}
    for url in args:
        contents[url] = urllib2.urlopen(url).read()

    diff = difflib.unified_diff(contents[args[0]],
                                contents[args[1]],
                                fromfile=args[0],
                                tofile=args[1],
                                lineterm='')

    # output
    if options.command:

        template = """%(PS1)s diff <(curl --location %(fromfile)s 2> /dev/null) <(curl --location %(tofile)s 2> /dev/null)"""
        print template % dict(PS1='#',
                              fromfile=args[0],
                              tofile=args[1])

    print '\n'.join(list(diff))

if __name__ == '__main__':
    main()
