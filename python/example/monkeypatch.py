#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys

__all__ = ['main']

class ExampleClass(object):
    def __init__(self, to_patch):
        if to_patch:
            self.output = lambda x, y: 'Patched!'
    def output(self, x, y):
        return '[{}] "{}"'.format(x, y)


if __name__ == '__main__':
    obj = ExampleClass(False)
    print (obj.output(1, 2))
    newobj = ExampleClass(True)
    print (newobj.output(3, 4))
