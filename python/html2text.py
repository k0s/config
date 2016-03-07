#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
convert HTML to text using only HTMLParser
"""

# imports
import argparse
import sys
from HTMLParser import HTMLParser

class HTML2Text(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.in_body = False
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.in_body = True

    def handle_data(self, data):
        if self.in_body:
            data = data.strip()
            if data:
                self.text.append(data)

    def __str__(self):
        return '\n'.join(self.text)

def main(args=sys.argv[1:]):

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin,
                        help='input file, or read from stdin if ommitted')
    options = parser.parse_args(args)

    # parse HTML
    html = options.input.read()
    html_parser = HTML2Text()
    html_parser.feed(html)
    html_parser.close()

    # output it
    print (html_parser)

if __name__ == '__main__':
    main()
