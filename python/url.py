#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
url manipulation
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import urlparse
import urllib2

__all__ = ['load', 'main']
string = (str, unicode)

def ensure_dir(directory):
    """ensure `directory` is a directory"""
    if os.path.exists(directory):
        assert os.path.isdir(directory)
        return directory
    os.makedirs(directory)
    return directory

def isURL(url):
    return '://' in url

def read_s3(url):
    name = tempfile.mktemp()
    try:
        subprocess.check_output(['s3cmd', 'get', url, name])
        with open(name) as f:
            read = f.read()
        os.remove(name)
        return read
    finally:
        if os.path.exists(name):
            os.remove(name)

def read_http(url):
    return urllib2.urlopen(url).read()

def read_file(url):
    scheme = 'file://'
    if url.startswith(scheme):
        url = url[len(scheme):]
    return open(url).read()

loaders = {'s3': read_s3,
           'http': read_http,
           'https': read_http,
           'file': read_file
       }

def scheme(url):
    if '://' in url:
        parsed = urlparse.urlsplit(url)
        return parsed.scheme
    return 'file'

def parent(url):
    if '://' in url:
        return url.rsplit('/', 1)[0]
    else:
        # file
        return os.path.abspath(os.path.dirname(url))

def basename(url):
    if '://' in url:
        return url.rsplit('/', 1)[-1]
    else:
        # file
        return os.path.basename(url)

def loader(url):
    return loaders[scheme(url)]

def load(url):
    """returns the contents of a URL"""
    return loader(url)(url)

def get_file(src, dest):
    shutil.copy2(src, dest)

def get_s3(src, dest):
    subprocess.check_output(['s3cmd', 'get', src, dest])

def default_getter(src, dest):
    assert not os.path.isURL(dest)
    dirname = parent(dest)
    ensure_dir(dirname)
    with open(dest, 'w') as f:
        f.write(load(url))

getters = {'file': get_file,
           's3': get_s3
       }

def get(src, dest):
    """get a thing to a local file"""
    if os.path.isdir(dest):
        dest = os.path.join(dest, basename(src))
    return getters.get(scheme(src), default_getter)(src, dest)

def rel(base, path):
    """
    relative path to base
    otherwise, return None
    """

    if path.startswith(base):
        return path[len(base):]

def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url', help='URL to read')
    parser.add_argument('-o', '--output', dest='output',
                        help="get to this location")
    options = parser.parse_args(args)

    if options.output:
        # copy src to this location
        get(options.url, options.output)
        sys.exit()

    # read location
    contents = load(options.url)

    # output
    print (contents)

if __name__ == '__main__':
    main()
