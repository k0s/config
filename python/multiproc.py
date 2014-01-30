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

progs = {'yes': ["yes"],
         'ping': ['ping', 'google.com']}

def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line
    usage = '%prog [options]'
    parser = argparse.ArgumentParser(usage=usage, description=__doc__)
    parser.add_argument("-t", "--time", dest="time",
                        type=float, default=4.,
                        help="seconds to run for")
    parser.add_argument("-s", "--sleep", dest="sleep",
                        type=float, default=1.,
                        help="")
    options = parser.parse_args(args)


    # select program
    prog = progs['ping']

    # start the main subprocess loop
    # TODO -> OO
    output = tempfile.SpooledTemporaryFile()
    start = time.time()
    proc = subprocess.Popen(prog, stdout=output)
    location = 0
    while proc.poll() is None:
        curr_time = time.time()
        run_time = curr_time - start
        if run_time > options.time:
            proc.kill()
        if options.sleep:
            time.sleep(options.sleep)
        output.seek(location)
        read = output.read()
        location += len(read)
        print ('[{}] {}\n{}'.format(run_time, read, '-==-'*10))

    # reset tempfile
    output.seek(0)

    n_lines = len(output.read().splitlines())
    print ("{}: {} lines".format(subprocess.list2cmdline(prog), n_lines))

if __name__ == '__main__':
    main()
