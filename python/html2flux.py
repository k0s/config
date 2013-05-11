#!/usr/bin/env python

"""
transform an HTML <dl> file into a fluxbox menu
if no file give, read from stdin

<dl><a>submenu name</a>
  <dt>program label</dt><dd>command</dd>
  <dt>another program label</dt><dd>command2</dd>
</dl>

x-form -> internal format:

('submenu name': [('program label', 'command'),
                  ('another program label', 'command2')])
"""

import optparse
import sys
from lxml import etree
from lsex import lsex # local import

# available executables
executables = set([i.rsplit('/', 1)[-1] for i in lsex() ])

def readmenu(dl, output, top=True):

    menu_items = []
    name = None # menu name
    for child in dl.iterchildren():

        if not top and child.tag == 'a':
            # TODO: better way of labeling this!
            print >> output, '[submenu] (%s)' % child.text

        if child.tag == 'dt':
            # item label
            label = ' '.join([i.strip() for i in child.itertext() if i.strip()])
        if child.tag == 'dd':
            command = ' '.join([i.strip() for i in child.itertext() if i.strip()])
            executable = command.split()[0]
            if executable in executables or os.path.isabs(executable):
                print >> output, '[exec] (%s) {%s}' % (label, command)

        if child.tag == 'dl':
            printmenu(child, output, top=False)
    if not top:
        print >> output, '[end]'

def printmenu(dl, output):
    """
    - output: file-like object for writing
    """
    menu = readmenu(dl, output)

def main(args=sys.argv[1:]):
    """command line interface"""

    # parse command line option
    usage = '%prog [options] [menu.html]'
    parser = optparse.OptionParser(usage=usage,
                                   description=__doc__)
    parser.add_option('--collapse', dest='collapse',
                      action='store_true', default=False,
                      help="collapse menus with a single item to that item")
    parser.add_option('-o', '--output', dest='output',
                      help="output file [Default: <stdout>]")
    options, args = parser.parse_args(args)

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

    # print to stdout
    printmenu(dl, fluxout)

if __name__ == '__main__':
    main()
