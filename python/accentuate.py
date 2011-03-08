#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

mapping = {'a': ['Ȁ', 'ȁ', 'à'],
           'c': ['ç'],
           'e': ['ȅ'],
           'n': ['И'], 
           'o': ['ổ', 'ȍ'],
           't': ['Ṱ'],
           }

if __name__ == '__main__':
    import sys
    arg = ' '.join(sys.argv[1:])
    retval = []
    for letter in arg:
        if letter.lower() in mapping:
            retval.append(random.sample(mapping[letter.lower()], 1)[0])
        else:
            retval.append(letter)
    print ''.join(retval)
