#!/usr/bin/env python

class Foo(object):
    def __call__(self, string):
        print string
    def __del__(self):
        print "Deleting"

foo = Foo()
foo("You will see deleting")
del foo

foo = Foo()
del Foo.__del__
foo("And now you won't")
del foo
