class fireonce(object):
    def __init__(self, func):
        self.func = func
    def __call__(self, *args, **kwargs):
        if not self.func:
            return None
        retval = self.func(*args, **kwargs)
        self.func = None

@fireonce
def foo(x):
    print x
    
foo('bar')
foo('fleem') # not printed
