#!/usr/bin/env python

"""
illustrate how classes work
"""

class A:
    pass

tests = ["issubclass(A(), A)",
         "issubclass(A, A)"]

if __name__ == '__main__':
    for test in tests:
        print ("? {}".format(test))
        try:
            print (eval(test))
        except Exception as e:
            print ('{}'.format(repr(e)))
