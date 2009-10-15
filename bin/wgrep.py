#!/usr/bin/env python

import sys
import urlparse
import urllib2
import tempfile
import shutil
import subprocess

def usage():
    print 'Usage: %s <url> <pattern>' % sys.argv[0]
    sys.exit(0)

def geturl(origurl):
    # get the url
    url = urlparse.urlsplit(origurl)
    if not url[0]:
        url = urlparse.urlsplit('http://%s' % origurl)
    return url

if __name__ == '__main__':
    if len(sys.argv[1:]) != 2:
        usage()
    urlparts = geturl(sys.argv[1])
    url = urlparse.urlunsplit(urlparts)

    # ensure the url is openable
    try:
        u = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print '%s\n%s' % (url, e)
        sys.exit(1)

    thedir = tempfile.mkdtemp()

    # wget the files
    wget = subprocess.Popen(['wget', '-r', '-l0',
                             '--no-parent',
                             '--no-check-certificate',
                             '-P', thedir,
                             u.url],
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE,
                            )
    out, err = wget.communicate()
    code = wget.returncode
    if code:
        sys.exit(code)

    # do da grep
    grep = subprocess.Popen(['grep', '-r', '-l', 
                             sys.argv[2], 
                             thedir],
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE,
                            )
    out, err = grep.communicate()
    for i in out.split('\n'):
        print i.replace('%s/' % thedir, '%s://' % urlparts[0], 1)

    destructive = True
    if destructive:
        shutil.rmtree(thedir)
    else:
        print thedir
