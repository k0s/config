#!/usr/bin/env python

"""
diff files over ssh
"""

import os
import subprocess
import sys
import tempfile
from optparse import OptionParser

def main(args=sys.argv[1:]):
    usage = "%prog host file"
    parser = OptionParser(usage=usage, description=__doc__)
    options, args = parser.parse_args(args)
    try:
        host, filename = args
    except ValueError:
        parser.print_usage()
        parser.exit(1)
    process = subprocess.Popen(["ssh", host, "cat", filename], stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    fd, buffer = tempfile.mkstemp()
    os.write(fd, stdout)
    os.close(fd)
    subprocess.call(['diff', os.path.join(os.environ['HOME'], filename), buffer])
    try:
        os.remove(buffer)
    except:
        pass

if __name__ == '__main__':
    main()
    
