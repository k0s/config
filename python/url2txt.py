#!/usr/bin/env python

# TODO: add url2txt as pluggable thingy for smartopen

# xclip -o | sed 's/_//' | sed 's/.html//'

def url2txt(url):
    """gets the text equivalent of a URL"""
    url = url.rstrip('/')
    if '/' in url:
        url = url.rsplit('/')[-1]
    if '.' in url:
        url = url.split('.', 1)[0]
    url = url.replace('_', ' ')
    return url

if __name__ == '__main__':
    import sys
    print url2txt(' '.join(sys.argv[1:]))
