#!/usr/bin/env python

"""
pypi strawman that should really be in PaInt

ref http://wiki.python.org/moin/PyPIJSON
"""

import json
import optparse
import os
import sys
import textwrap
import urllib2

def package_data(package, index='http://pypi.python.org/pypi'):
    """
    returns dict of {url:, description:, home_page: }
    """

    # if package name given, -> url
    url = package
    if '://' not in url:
        url = '%s/%s' % (index, package)
    url = url.rstrip('/')

    if not url.endswith('/json'):
        url = '%s/json' % (url)

    # read the URL
    try:
        page = urllib2.urlopen(url).read()
    except:
        raise # TODO: better error handling

    data = json.loads(page)
    info = data['info']

    # massage the data
    return {'summary': info.get('summary', ''),
            'package_url': info['package_url'],
            'name': info['name'],
            'home_page': info.get('home_page')
    # etc
            }


def main(args=sys.argv[1:]):

    # command line parser
    usage = '%prog [options] package <another_package> <...>'
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    parser.add_option('-t', '--tag', dest='tags',
                      action='append', help="tags for packages")
    options, args = parser.parse_args(args)
    if not args:
        parser.print_usage()
        parser.exit()

    # one crappy ass template
    template = """ * %(package_url)s
%(summary)s
  %(tags)s
"""

    # get package data
    packages = {}
    for package in args:
        data = package_data(package)
        packages[data['name']] = data

    # render the damn thing
    rendered = []
    for name in sorted(packages.keys(), key=lambda x: x.lower()):
        values = packages[name].copy()
        if options.tags:
            values['tags'] = '{%s}' % ', '.join(options.tags)
        else:
            values['tags'] = ''
        if values['home_page'] and values['home_page'] != values['package_url']:
            values['summary'] = '%s %s' % (values['summary'],
                                               values['home_page'])
            values['summary'] = textwrap.fill(values['summary'], 69,
                                              initial_indent='  ',
                                              subsequent_indent='  ')
        string = template % values
        rendered.append(string.strip())

    print '\n\n'.join([i.strip() for i in rendered])

if __name__ == '__main__':
    main()
