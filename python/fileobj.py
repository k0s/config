#!/usr/bin/env python

"""
filename -> file-like object as a decorator
"""

import optparse
import os
import sys

string = (basestring,)

class fileobj(object):
    def __init__(self, arg, *args, **kwargs):
        self._args = [arg] + list(args)
        self._kwargs = kwargs
        # mode, filename, ...

        # function
        self.func = arg if not args else None
    def __call__(self, *args, **kwargs):
        if self.func is None:
            raise NotImplementedError
        else:
            if len(args) and isinstance(args[0], string):
                args = list(args)
                with file(args[0], 'w') as fp:
                    args[0] =fp
                    return self.func(*args, **kwargs)
            return self.func(*args, **kwargs)

if __name__ == '__main__':
    # test code
    import os
    import tempfile

    @fileobj
    def test1(fp):
        fp.write('foo')

    filename = tempfile.mktemp()
    print filename
    assert not os.path.exists(filename)
    test1(filename)
    assert os.path.exists(filename)
    print file(filename).read()
