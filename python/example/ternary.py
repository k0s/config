#!/usr/bin/env python

"""
illustrates python ternary is smart about branching
"""

class Foo(object):
    def __init__(self):
        print 'hi'
bar = 1
print Foo() if bar is None else bar
