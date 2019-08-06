#!/usr/bin/env python

divider = ':'

def dictify(string):
    lines = [ i.strip() for i in string.split('\n') if i.strip() ]
    return dict([i.split(divider,1) for i in lines
                 if len(i.split(divider,1)) == 2])

if __name__ == '__main__':
    import sys
    feh = sys.stdin.read()
    thedict = dictify(feh)
    if sys.argv[1:]:
        for i in sys.argv[1:]:
            if i in thedict:
                print (thedict[i])
    else:
        print (thedict)
