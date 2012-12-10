#!/usr/bin/env python

def prime(number):
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
    import sys
    for arg in sys.argv[1:]:
        print prime(int(arg))
