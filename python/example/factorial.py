#!/usr/bin/env python
"""how many 0s are in a factorial"""

import argparse
import sys

def factorial(N):
    """factorial of `N`"""
    if N == 1:
        return 1
    return reduce(int.__mul__, range(2, N+1))

def factorial_zeros(N):
    """how many 0s are in a factorial?"""

    return N/5

def main(args=sys.argv[1:]):
    """CLI"""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('N', type=int, nargs='+')
    options = parser.parse_args(args)

    # sanity
    if any([i < 1 for i in options.N]):
        parser.error("Input values must be >= 1")

    for i in options.N:
        f =  factorial(i)
        print f

if __name__ == '__main__':
    main()
