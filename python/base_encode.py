#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
arbitrary base encoding tools (convert number <=> string)

modified from
https://gist.github.com/adyliu/4494223
"""

import argparse
import string
import sys

basedigits = string.digits + string.letters

def decode(s, basedigits=basedigits):

    BASE = len(basedigits)
    ret,mult = 0,1
    for c in reversed(s):
        ret += mult*basedigits.index(c)
        mult *= BASE
    return ret

def encode(num, basedigits=basedigits):
    BASE = len(basedigits)

    if num < 0:
        raise Exception("positive number "+num)
    if num == 0:
        return '0'
    ret=''
    while num:
        ret = (basedigits[num%BASE])+ret
        num = int(num/BASE)
    return ret


def main(args=sys.argv[1:]):

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('num', nargs='+',
                        help="num")
    parser.add_argument('-b', '--base', dest='base',
                        type=int, default=32,
                        help="base to use [DEFAULT: %(default)s]")
    parser.add_argument('-c', '--chars', '--base-digits', dest='basedigits',
                        default=globals()['basedigits'],
                        help="base digits [DEFAULT: %(default)s]")
    options = parser.parse_args(args)

    # determine base digits
    basedigits = options.basedigits[:options.base]
    base = len(basedigits)

    for num in options.num:

        try:
            num = int(num)
            encoded = encode(num, basedigits)
            print ('ENCODE base {}: {}->{} [{}]'.format(base, num, encoded, len(encoded)))
        except ValueError:
            print ('%*s %s %s' % ('DECODE', num, decode(num)))

if __name__ == '__main__':
    main()
