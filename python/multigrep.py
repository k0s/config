#!/usr/bin/env python

"""
grep through multiple directories
"""

# TODO: use a python grep implemention v subshell (probably)

import optparse
import os
import subprocess
import sys

def main(args=sys.argv[1:]):

    # CLI
    usage = '%prog [options] PATTERN DIRECTORY [DIRECTORY] [...]'
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    parser.add_option('-f', '--files', dest='files', default='*',
                      help="file pattern [DEFAULT: %default]")
    parser.add_option('-g', '--grep', dest='grep',
                      action='append', default=[],
                      help="`grep` command [DEFAULT: grep]")
    parser.add_option('-p', '--print', dest='print_commands',
                      action='store_true', default=False,
                      help="print grep commands to run and exit")
    options, args = parser.parse_args(args)
    if len(args) < 2:
        parser.print_help()
        parser.exit()
    options.grep = options.grep or ['grep']
    pattern, directories = args[0], args[1:]

    # verify directories
    missing = [i for i in directories
              if not os.path.isdir(i)]
    if missing:
        sep = '\n  '
        parser.error("Not a directory:%s%s" % (sep, sep.join(missing)))

    # build command line
    command = options.grep[:]
    command.extend([pattern, options.files])
    cwd = os.getcwd()

    if options.print_commands:
        # print grep commands
        for directory in directories:
            print "cd %s; %s" % (repr(directory), subprocess.list2cmdline(command))
        print "cd %s" % (repr(cwd))
        parser.exit()

    # loop through directories
    for directory in directories:
        print directory
        subprocess.call(subprocess.list2cmdline(command),
                        cwd=directory,
                        shell=True)

if __name__ == '__main__':
    main()
