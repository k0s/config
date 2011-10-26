#!/usr/bin/env python

import os

def extensions(*filenames):
    return set([os.path.splitext(f)[-1] for f in filenames
                if '.' in f])

def find_extensions(*directories):
    _extensions = set()
    for directory in directories:
        for _, _, fnames in os.walk(directory):
            _extensions.update(extensions(*fnames))
    return _extensions
        
if __name__ == '__main__':
    import sys
    for ext in sorted(find_extensions(*sys.argv[1:])):
        print ext
