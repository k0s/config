#!/usr/bin/env python

"""
wait for a process writing to stdout to keep an
(e.g.) ssh connection alive
"""

import subprocess
import sys
import time

KEEPALIVE = 300  # s
SLEEP = 1


def main(args=sys.argv[1:]):
    """CLI"""

    last = start = time.time()
    proc = subprocess.Popen(args)

    while proc.poll() is None:
        if time.time() - last > KEEPALIVE:
            last = time.time()
            print ("[{} s] waiting for process: {}".format(last-start, subprocess.list2cmdline(args)))
            sys.stdout.flush()
    exit(proc.poll())

if __name__ == '__main__':
    main()
