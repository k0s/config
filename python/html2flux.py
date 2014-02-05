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
import os
import sys
from lxml import etree
from lsex import lsex # local import

# available executables
executables = set([i.rsplit('/', 1)[-1] for i in lsex() ])

# TODO: next generation
# class HtmlMenu
#     def  _init__(self, html):
#         if isinstance (html, string):
#             html =
#         for item in html

# class Command
#     classname = ''

# class Sudo(Command)
#     classname = 'sudo'
#     programs = (('gksudo',),)

def readmenu(dl, output, top=True):
    """read menu from an <dl> tag"""
    # TODO: probably don't really need lxml

    menu_items = []
    name = None # menu name
    firstchild = True
    label = None
    for child in dl.iterchildren():

        if not top and child.tag == 'a' and firstchild:
            # TODO: better way of labeling this!
            name = child.text.strip()

        if child.tag == 'dt':
            # item label
            label = ' '.join([i.strip() for i in child.itertext() if i.strip()])
        if child.tag == 'dd':
            # command
            command = ' '.join([i.strip() for i in child.itertext() if i.strip()])
            # TODO: classes
            executable = command.split()[0]
            if executable in executables or os.path.isabs(executable):
                menu_items.append((label, command))

        # submenu
        if child.tag == 'dl':
            menu_items.append(readmenu(child, output, top=False))

    return (name, menu_items)

def printflux(name, menu, output, top=True):
    """
    - output: file-like object for writing
    """

    # print [submenu] tag for this menu
    name = name or ''
    if not top:
        print >> output, '[submenu] (%s)' % name

    # print menu items
    for name, item in menu:
        if isinstance(item, basestring):
            # command
            print >> output, '[exec] (%s) {%s}' % (name, item)
        else:
            # submenu
            printflux(name, item, output, top=False)

    # print end of this submenu
    if not top:
        print >> output, '[end]'

def printmenu(dl, output):
    name, menu = readmenu(dl, output)
    printflux(name, menu, output)

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
