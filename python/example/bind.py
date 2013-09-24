#!/usr/bin/env python

"""
illlustrate e.g. method bind for python
"""

class Foo(object):

    @classmethod
    def create(cls):
        """create an instance and bind a method onto foo"""
        class decorator(object):
            def __init__(self, function):
                self.function = function
            def __call__(self):
                print "Bar!"
                return self.function()

        instance = cls()
        instance.foo = decorator(instance.foo)
        return instance

    def foo(self):
        print "Foo!"

if __name__ == '__main__':
    foo = Foo.create()
    foo.foo()
