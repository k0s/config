#!/usr/bin/env python

def onelineit(string):
    string = string.split('\n')
    string = [ i.strip() or '\n' for i in string ]
    string = ' '.join(string)
    string = string.split('\n')
    string = [ i.strip() for i in string if i.strip() ]

    return '\n\n'.join(string)

if __name__ == '__main__':
    import sys    
    print onelineit(sys.stdin.read())
