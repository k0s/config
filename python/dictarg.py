#!/usr/bin/python

import sys

def dictarg(adict, argv=sys.argv[1:]):

    shopts = {}
    
    # build list of keys
    for i in adict.keys():
        for j in i:
            s = str(j)
            if len(s) == 1:
                if shopts.has_key(s):
                    continue
                shopts[s] = i
                break
        else:
            print >> sys.stderr, "dictarg: couldn't generate key for '%s'" % i
            sys.exit(1)

    optstring = "?"
    for i in shopts.keys():
        optstring += i + ':' # all these options should have arguments
    
    # look for command line args
    import getopt

    opts, args = getopt.getopt(argv, optstring)

    if ('-?', '') in opts:
        print 'Options:'
        for i in shopts:
            print '-%s %s [%s]' % (i, shopts[i], adict[shopts[i]])
        sys.exit(0)
        
    for o, v in opts:
        o = o[1:] # cut off the dash
        adict[shopts[o]] = v

# test if invoked from command line
if __name__ == '__main__':
    adict = {}
    for i in sys.argv:
        adict[i] = len(i)

    # print the help
    dictarg(adict, ['-?'])

    # test functionality
    print 'Enter test arguments: ',
    line = sys.stdin.readline()[:-1].split(' ')
    dictarg(adict, line)
    print adict
