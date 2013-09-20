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
    return [i for i in subprocess.check_output(['find', directory, '-iname', patten]).splitlines() if i.strip()]
    
def rejects(directory):
    """all rejects in directory"""
    # TODO: not call out to find
    

def main(args=sys.argv[1:]):

    usage = '%prog [options]'
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    parser.add_option('-d', '--directory', default=os.getcwd())
    options, args = parser.parse_args(args)

    

if __name__ == '__main__':
    main()
