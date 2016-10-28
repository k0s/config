#!/usr/bin/env python

"""
print prime numbers for each argument given
"""

def prime(number):
    """determines if `number` is prime"""
    # XXX this is owefully inefficient and is written as
    # a (bad) example only

    half = int(number / 2)
    for i in range(2, half):
        if not number % i:
            return False
    return True

def primes(n):
    return [i for i in range(2,n)
            if not [True for j in range(2,1 + i/2)
                    if not i%j]]


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('arg', type=int, nargs='+',
                        help="(positive) integer to find the primes for")
    options = parser.parse_args()
    for arg in options.arg:
        print prime(arg)
