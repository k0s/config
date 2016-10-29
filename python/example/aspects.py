class MakePythonLikeJavascript(object):
    def __getattr__(self, name):
        return undefined

class undefined(MakePythonLikeJavascript):
    def __nonzero__(self):
        return False
    def __str__(self):
        return 'undefined'
    __repr__ = __str__
undefined = undefined() # singleton

if __name__ == '__main__':
    foo = MakePythonLikeJavascript()
    foo.bar = 5
    print foo.bar
    print foo.fleem
    print foo.fleem.flarg
