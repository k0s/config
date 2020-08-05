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

     - add graphterm: graphterm (should be in ~/k0s/)
       * if a menu has a single item, that is *the* implementor to that interface! :)
     - display fluxbox menu items by `title` attribute, if possible
       * (see class-based usage below)
     - something about && for joining
     - class-based usage (class="shell|...")
       * and is the shell persistent? small? etc.
       * also, sudo! (or other access related thing)
       * resolve: xmessage v gmessage v xosd_cat etc
       * classes: shell, root, message
     - an easier way of editing o_O
       * add an item to a menu
       * submenu
     - utility to find missing commands
     - utility to add command + (e.g. ubuntu) install
     - python package for all of this
       * ...which also sets up the whole html2flux thing
     - ....and the 50 billion dollar problem is:
       How to integrate $(this) and http://k0s.org/portfolio/ubuntu-packages.txt
       * these should have classifiers and ultimately work in to toolbox
     - can a workflow be mapped to a (X; and, tbf, hierarchal) menu?!?
       * YOU'RE SEEING IT, RIGHT?
     - that said, a hierachal menu...ain't the best; maybe something like
       dasher....
     - to that effect, amonst others, menu items of the same set
       should be added multiple places.  that is to say, the menu item
       indicated as `[foo][bar]fleem` could also live under
       `[bar][foo]fleem`
"""

import argparse
import os
import sys
from lxml import etree
from lsex import lsex # local import

try:
    # python2
    string = (str, unicode)
except NameError:
    # python3
    string = (str,)

# available executables
executables = set([os.path.basename(i) for i in lsex() ])

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
    print menu in fluxbox notation

    - output: file-like object for writing
    """

    if not menu:
        return

    # print [submenu] tag for this menu
    name = name or ''
    if not top:
        output.write('[submenu] (%s)\n' % name)

    # print menu items
    for name, item in menu:
        if isinstance(item, string):
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
    if isinstance(output, string):
        with open(output, 'w') as f:
            printflux(name, menu, f)
    else:
        # file-like object
        printflux(name, menu, output)

def main(args=sys.argv[1:]):
    """command line interface"""

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('htmlfile', metavar='programs.html', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin,
                        help='input file, or read from stdin if ommitted')
    parser.add_argument('--collapse', dest='collapse',
                      action='store_true', default=False,
                      help="collapse menus with a single item to that item")
    parser.add_argument('-o', '--output', dest='output',
                      help="output file [Default: <stdout>]")
    options = parser.parse_args(args)

    # read input
    html = options.htmlfile.read()

    # get first element
    dom = etree.fromstring(html)
    dl = dom.find('.//dl')

    # print to stdout
    printmenu(dl, options.output or sys.stdout)

if __name__ == '__main__':
    main()
