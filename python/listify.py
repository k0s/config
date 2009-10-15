def listify(listitems, ordered=False):
    """ return an html list """
    if not hasattr(listitems, '__iter__'):
        thelist = ( listitems, )
    if ordered:
        tag, invtag = '<ol>\n', '</ol>'
    else:
        tag, invtag = '<ul>\n', '</ul>'

    thelist = tag
    
    for i in listitems:
        thelist += ' <li> ' + str(i) + ' <li>\n'

    thelist += invtag
    return thelist

if __name__ == '__main__':
    import sys
    print listify(sys.argv)
