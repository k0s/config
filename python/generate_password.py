#!/usr/bin/env python

import random
import string
import sys

pool = ''.join([string.ascii_letters,
                string.digits,
                string.punctuation])

contents = [(string.ascii_lowercase, 6),
            (string.ascii_uppercase, 6),
            (string.punctuation, 2)]

def password(length=16, pool=pool):
    return ''.join(random.sample(pool, length))

def main(args=sys.argv[1:]):
    """CLI"""

    print(password())
    
if __name__ == '__main__':
    main()
