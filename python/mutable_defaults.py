#!/usr/bin/env python

# see also: http://www.daniweb.com/software-development/python/threads/66697

class Foo(object):
  def __init__(self, mutable=['default']):
    self.foo = mutable
    self.foo.append(1)

if __name__ == '__main__':
  bar = Foo()
  print len(bar.foo)
  fleem = Foo()
  print len(fleem.foo)
  assert len(fleem.foo) == 2, "Don't use default mutable arguments!"
