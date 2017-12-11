#!/usr/bin/env python

"""
password generator
"""

import argparse
import random
import string
import sys


def generate_password(population=string.ascii_letters+string.digits,
                      length=12):
    """
    returns a random password `length` characters long
    sampled from `population`
    """

    return ''.join(random.sample(population, length))


def main(args=sys.argv[1:]):

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-l', '--length', dest='length',
                        type=int, default=12,
                        help="length of password to generate [DEFAULT: %(default)s]")
    options = parser.parse_args(args)

    # print generated password
    print (generate_password(length=options.length))

if __name__ == '__main__':
    main()
