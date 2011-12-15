#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

mapping = {'a': ['Ȁ', 'ȁ', 'à', 'Ѧ', 'ª', 'Å', 'Ą'],
           'b': ['Б', 'ß'],
           'c': ['ç'],
           'd': ['Ð', 'đ'],
           'e': ['ȅ', 'Ё', 'Є', 'Ę'],
           'i': ['ו', 'ḯ', 'í'],
           'l': ['£', '₤'],
           'n': ['И', 'Й', 'א'],
           'o': ['ổ', 'ȍ', 'Ѳ'],
           's': ['∫', '§'],
           't': ['Ṱ', 'ל'],
           'u': ['ṹ'],
           'v': ['Ѵ'],
           'w': ['Ѡ', 'Щ', 'ש'],
           'z': ['ź'],
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
