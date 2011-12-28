
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

if __name__ == '__main__':
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
    a.foo(1)


