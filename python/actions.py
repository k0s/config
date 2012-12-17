#!/usr/bin/env python

class Actions(object):

    def __init__(self):
        self.functions = {}

    def __call__(self, function):
        return function

action = Actions()

@action
def foo():
    print "hello"

@action
def bar():
    print "goodbye"

if __name__ == '__main__':
    pass
