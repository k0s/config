#!/usr/bin/env python

import sys

def filename(dotpath):
    path = dotpath.split('.')
    while path:
        try:
            module = __import__('.'.join(path))
            return module.__file__.rstrip('c')
        except ImportError:
            path.pop()

def main(args=sys.argv[1:]):
    for arg in args:
        try:
            _filename = filename(arg)
        except Exception, e:
            print e
            continue
        print _filename

if __name__ == '__main__':
    main()
