#!/usr/bin/env python

def prime(number):
    half = int(number / 2)
    for i in range(2, half):
        if not number % i:
            return False
    return True

if __name__ == '__main__':
    import sys
    for arg in sys.argv[1:]:
        print prime(int(arg))
