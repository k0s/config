#!/usr/bin/env python

class Actions(object):

    def __init__(self):
        self.functions = {}

    def __call__(self, function, dependencies):
        import pdb; pdb.set_trace()
        self.functions[function.func_name] = function
        return function

    def do(self, func_name):
        self.functions[func_name]()

action = Actions()

@action
def foo():
    print "hello"

@action('foo')
def bar():
    print "goodbye"

if __name__ == '__main__':
    pass

action.do('bar')
