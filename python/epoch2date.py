#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
conversion between epoch and dates

https://docs.python.org/2/library/time.html
https://docs.python.org/2/library/datetime.html
"""

# TODO: tz info
#http://bugs.python.org/issue7229
# http://stackoverflow.com/questions/13218506/how-to-get-system-timezone-setting-and-pass-it-to-pytz-timezone


import argparse
import datetime
import os
import subprocess
import sys
import time

def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('seconds_since_epoch',
                        type=float, nargs='?', default=time.time(),
                        help="seconds since epoch input [DEFAULT: %(default)s]")
    options = parser.parse_args(args)

    # produce a datetime
    dt = datetime.datetime.fromtimestamp(options.seconds_since_epoch)
    dt2 = datetime.datetime.utcfromtimestamp(options.seconds_since_epoch)

    # output
    print ("{} seconds since epoch".format(options.seconds_since_epoch))
    print ("{} {}".format(dt, time.tzname[time.daylight]))
    print ("{} UTC".format(dt2))

if __name__ == '__main__':
    main()
