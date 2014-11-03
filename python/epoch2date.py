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

try:
    # use dateutil parser if available
    from dateutil.parser import parse as parse_date
except ImportError:
    parse_date = None


def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('seconds_since_epoch',
                        type=float, nargs='*', default=time.time(),
                        help="seconds since epoch input [DEFAULT: %(default)s]")
    parser.add_argument('--utc', dest='display_utc',
                        action='store_true', default=False,
                        help="display UTC time only")
    options = parser.parse_args(args)

    if isinstance(options.seconds_since_epoch, float):
        options.seconds_since_epoch = [ options.seconds_since_epoch ]

    for s in options.seconds_since_epoch:

        # produce a datetime
        dt = datetime.datetime.fromtimestamp(s)
        dt2 = datetime.datetime.utcfromtimestamp(s)

        # output
        if not options.display_utc:
            print ("{} seconds since epoch".format(s))
            if time.daylight and time.localtime(s).tm_isdst:
                tz_index = 1
            else:
                tz_index = 0
            print ("{} {}".format(dt, time.tzname[tz_index]))
        print ("{} UTC".format(dt2))

if __name__ == '__main__':
    main()
