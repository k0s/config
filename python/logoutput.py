#!/usr/bin/env python

"""
execute a command and log its output to a file
"""

import sys
from subprocess import list2cmdline, STDOUT
from subprocess import check_output as call

def main(args=sys.argv[1:]):
    """CLI"""

    usage = '%prog outputfile command [args]'
    usage += '\n' + __doc__
    if args < 2:
        print 'Usage: ' + usage
        sys.exit(1)

    path = args.pop(0)
    commandline = list2cmdline(args)

    with file(path, 'w') as w:
        output = call(args, stderr=STDOUT)
        w.write('\n\n'.join([commandline, output]))

if __name__ == '__main__':
    main()
