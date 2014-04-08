#!/usr/bin/env python

import sys

def hexify(string, excludes=('/',)):
    return ''.join([i if i in excludes else ('%'+ hex(ord(i))[-2:])
                    for i in string])

def hidden_url(string):
    if '://' in string:
        scheme, rest = string.split('://', 1)
        if '/' in rest:
            loc, rest = rest.split('/', 1)
            return '{}://{}/{}'.format(scheme, loc, hexify(rest, excludes=('/',)))
        else:
            return string
    else:
        return hexify(string, excludes=('/',))

def main(args=sys.argv[1:]):
    string = ' '.join(args)
    print hidden_url(string)

if __name__ == '__main__':
    main()
