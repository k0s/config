#!/usr/bin/env

"""
demo related to abstract classes
"""

### roll our own to demo

def abstractmethod(method):
    line = method.func_code.co_firstlineno
    filename = method.func_code.co_filename
    def not_implemented(*args, **kwargs):
        raise NotImplementedError('Abstract method %s at File "%s", line %s should be implemented by a concrete class' % (repr(method), filename, line))
    return not_implemented

class AbstractBaseClass(object):

    @abstractmethod
    def foo(self, arg):
        """foo does such and such"""

    @abstractmethod
    def bar(self):
        """bar does something else"""

class ConcreteClass(AbstractBaseClass):

    def foo(self, arg):
        print 'hello'


### now use the abc module

import abc

class AbstractClass(object):
    @abc.abstractmethod
    def foo(self, arg):
        """blah"""
    @abc.abstractmethod
    def bar(self):
        """bar does nothing"""

class CementClass(AbstractBaseClass):
    def foo(self, arg):
        print 'goodbye'

class Picasso(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def foo(self, arg):
        """blah"""


if __name__ == '__main__':

    # home-rolled
    c = ConcreteClass()
    c.foo(1)
    a = AbstractBaseClass()
    try:
        a.foo(1)
    except NotImplementedError, e:
        print e
    try:
        a.bar()
    except NotImplementedError, e:
        print e
    c.foo(1)
    try:
        a.foo(1)
    except NotImplementedError, e:
        print e

    ### abc
    print '\nIllustrate `abc` functionality'
    a = AbstractClass()
    e = None
    try:
        a.foo(1)
        # you'd think this would raise an exception since`
        # `AbstractClass.foo` is decorated with `abc.abstractmethod`
        # But see http://docs.python.org/2/library/abc.html :
        # "Using this decorator requires that the class's metaclass
        # is ABCMeta or is derived from it."
    except Exception, e:
        pass
    assert e is None # !

    # as an aside, another good reason not to use super:
    # "Unlike Java abstract methods, these abstract methods may
    # have an implementation. This implementation can be called via the super()
    # mechanism from the class that overrides it. This could be useful as
    # an end-point for a super-call in a framework that uses cooperative
    # multiple-inheritance."

    a = Picasso()
    e = None
    try:
        a.foo(1)
    except Exception, e:
        pass
    import pdb; pdb.set_trace()
