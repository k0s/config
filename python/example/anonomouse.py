
def foo(a):

    c = ['hi']

    def bar(n):
        d = c[:][0].upper()
        return '{} {}!'.format(d, a) * n

    fleem = lambda n: '{} {}!'.format(c[:][0].upper(), a) * n

    c = ['hello']

    return (bar,
            fleem)

_bar, _fleem = foo("world")
print (_bar(2))
print (_fleem(2))
