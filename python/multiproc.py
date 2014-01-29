#!/usr/bin/env python

"""
multiprocessing/subprocess experiments
"""

import argparse
import os
import subprocess
import sys
import time
import tempfile

here = os.path.dirname(os.path.realpath(__file__))
prog = ["yes"]
timeout = 4.
sleep = 1.

def main(args=sys.argv[1:]):

    usage = '%prog [options]'
    parser = argparse.ArgumentParser(usage=usage, description=__doc__)
    parser.add_argument("-t", "--time", dest="time",
                        type=float, default=1.,
                        help="seconds to run for")
    options = parser.parse_args(args)

    output = tempfile.SpooledTemporaryFile()
    start = time.time()
    proc = subprocess.Popen(prog, stdout=output)
    while proc.poll() is None:
        if time.time() - start > options.time:
            proc.kill()

    # reset tempfile
    output.seek(0)

    n_lines = len(output.read().splitlines())
    print ("{}: {} lines".format(subprocess.list2cmdline(prog), n_lines))

if __name__ == '__main__':
    main()
