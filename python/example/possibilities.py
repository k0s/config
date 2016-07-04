#!/usr/bin/env python

"""
"""

# imports
import argparse
import sys
import time
from pprint import pprint

costs = {1:1,
         7:3,
         30:25}

A = [1, 2, 4, 5, 7, 29, 30]

def possibilities(A):
    possibilities = [[(1, date) for date in A]]
    for_consideration = [0]
    while True:
        if not for_consideration:
            break
        _for_consideration = []
        for item in for_consideration:
            basis = possibilities[item][:]
            tickets = [i[0] for i in basis]
            if set(tickets) == set([7]):
                continue
            index = 0
            potential = []
            while True:
                try:
                    pos = tickets.find(1, index)
                except ValueError:
                    break
                potential = basis[:]
                potential[pos] = (7, basis[pos][-1])

        try:
            while A[index] < date+6:
                index += 1
        except IndexError:
            pass

    return possibilities


def fill_space(A, spans):
    """
    A -- the space to be filled
    spans -- the discrete length of each space
    """
    if not A:
        return []

    A = sorted(A)

    possibilities = []

    # [(ticket_value, index_into_A)]
    working_set = [[(value, 0)] for value in spans]
    # print "working set"
    # pprint(working_set)
    while working_set:
        item = working_set.pop()
        last_span, index = item[-1]
        last_date = A[index]
        e = None
        index += 1
        try:
            while last_date + last_span > A[index]:
                # print ('index: {}'.format(index))
                index += 1
        except IndexError as e:
            possibilities.append(item)
            continue

        # print "item:"
        # pprint(item)
        extension = [item[:] + [(span, index)]
                     for span in spans]

        working_set.extend(extension)

    # fill possibility indices with dates
    retval = [[(A[index], span) for span, index in possibility]
              for possibility in possibilities]
    return retval


def sorted_costs(A, costs=tuple(costs.items())):

    costs = dict(costs)

    # determine possibility spaces
    spaces = fill_space(A, spans=costs.keys())

    # determine costs
    retval = []
    for space in spaces:
        cost = sum([costs[value] for date, value in space])
        retval.append((cost, space))

    # sort by cost
    retval.sort(key=lambda x: x[0])

    return retval

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=__doc__)
    options = parser.parse_args()

    dates = sorted(A)

    print "Dates: {}".format(', '.join([str(i) for i in dates]))
    for cost, value in sorted_costs(A, costs):
        print ("{} : {}".format(cost, value))
