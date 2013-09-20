#!/usr/bin/env python

# XXX STUB

"""
http://code.google.com/p/python-patch/
"""

import difflib
import optparse
import os
import subprocess
import sys
from which import which

here = os.path.dirname(os.path.realpath(__file__))

wiggle = which('wiggle')

def find(directory, pattern):
    # TODO: -> python
    return [i for i in subprocess.check_output(['find', directory, '-iname', pattern]).splitlines() if i.strip()]

def rejects(directory):
    """all rejects in directory"""
    # TODO: not call out to find
    return find(directory, '*.rej')

def main(args=sys.argv[1:]):

    usage = '%prog [options]'
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    parser.add_option('-d', '--directory', default=os.getcwd())
    options, args = parser.parse_args(args)

    # get rejects
    rej = rejects(options.directory)
    if not rej:
        parser.error("No rejects")
    print 'rej:\n%s\n' % '\n'.join([' %s' % r for r in rej])

    for r in rej:
        # find the corresponding file
        pass

if __name__ == '__main__':
    main()
