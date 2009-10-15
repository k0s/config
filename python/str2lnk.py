#!/usr/bin/python

def str2lnk(string):
    """transform a string to a legitimate link name for html"""
    illegal_characters=' @,?/\\#'
    for i in illegal_characters:
        string = string.replace(i, '_')
    newstring = ''
    for i in string.split('_'):
        if i:
            newstring += i + '_'
    return newstring[:-1]
    
if __name__ == '__main__':
    import sys
    try:
        newstring=sys.argv[1]
    except IndexError:
        print '%s' % str2lnk.__doc__
        print 'Usage: %s <string to be made a link>' % sys.argv[0]
        sys.exit(0)

    newstring = ' '.join(sys.argv)
    print str2lnk(newstring)
