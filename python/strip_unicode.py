#!/usr/bin/env python

import string
import sys


def main(args=sys.argv[1:]):

    if args:
        message = ' '.join(args)
    else:
        message = sys.stdin.read()

    print(''.join(i for i in message if i in string.printable))


if __name__ == '__main__':
    main()
