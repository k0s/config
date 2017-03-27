#!/usr/bin/env python

"""
given a `value` and an array,
if the sum of two numbers in the array
total the value, return `True`
(exit 0):

 ./array_sum.py 3 1 2 4  # YES!  because 1+2=3

 ./array_sum.py 4 1 2 5 6  # NO!
"""

import argparse
import sys


def sum_of_two(value, *array):

    start = 0
    end = len(array) - 1
    complements = []
    while start < end:
        start_val = array[start]
        end_val = array[end]
        _sum = start_val + end_val
        if _sum == value:
            complements.append((start_val, end_val))
            end -= 1
            start +=1
            continue
        if _sum > value:
            end -= 1
        else:
            start += 1
    return complements


def main(args=sys.argv[1:]):

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('value', type=int)
    parser.add_argument('array', type=int, nargs='+')
    options = parser.parse_args(args)

    retval = sum_of_two(options.value, *options.array)

    print (retval)

    sys.exit(0 if retval else 1)


if __name__ == '__main__':
    main()
