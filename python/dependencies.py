#!/usr/bin/env python

import imp
import os
import pprint
import sys

current_module = None
info = {}

def setup(**kwargs):
    assert current_module
    info[current_module] = kwargs

def main(args=sys.argv[1:]):

    global current_module
    current_module = None

    setuptools = sys.modules.get('setuptools')
    sys.modules['setuptools'] = sys.modules[__name__]

    try:
        for setup_py in args:
            current_module = setup_py
            assert os.path.exists(setup_py)
            module = imp.load_source('setup', setup_py)
    except:
        sys.modules.pop('setuptools')
        if setuptools:
            sys.modules['setuptools'] = setuptoools

    pprint.pprint(info)

if __name__ == '__main__':
    main()
