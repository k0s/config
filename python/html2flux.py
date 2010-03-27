#!/usr/bin/env python

import sys
from lxml import etree

from lsex import lsex # local import
executables = set([i.rsplit('/', 1)[-1] for i in lsex() ])

def printmenu(dl, output, top=True):
    
    # XXX should do more checking
    for child in dl.iterchildren():
        if not top and child.tag == 'a':
            print >> output, '[submenu] (%s)' % child.text
        if child.tag == 'dt':
            label = ' '.join([ i.strip() for i in child.itertext() if i.strip() ])
        if child.tag == 'dd':
            command = ' '.join([ i.strip() for i in child.itertext() if i.strip() ])
            executable = command.split()[0]
            if executable in executables:
                print >> output, '[exec] (%s) {%s}' % (label, command)
        if child.tag == 'dl':
            printmenu(child, output, top=False)
    if not top:
        print >> output, '[end]'

def main(args = sys.argv[1:]):

    # setup input, output
    if args:
        htmlfile = file(args[0])
    else:
        htmlfile = sys.stdin
    html = htmlfile.read()
    fluxout = sys.stdout

    # get first element
    dom = etree.fromstring(html)
    dl = dom.find('.//dl')

    printmenu(dl, fluxout)

if __name__ == '__main__':
    main()
