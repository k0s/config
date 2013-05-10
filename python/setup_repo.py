#!/usr/bin/env python

"""
setup a repository

Parameters:
- host URL
- location on host disk
"""

import os
import subprocess
import sys
import urlparse

from subprocess import check_call as call
from optparse import OptionParser


# global variables
HOST='k0s.org'
HGRC="""[paths]
default = http://%(host)s/%(repo)s/%(name)s
default-push = ssh://%(host)s/%(repo)s/%(name)s
"""

def call(command, *args, **kw):

    code = subprocess.call(command, *args, **kw)
    if isinstance(command, basestring):
        cmdstr = command
    else:
        cmdstr = ' '.join(command)
    print cmdstr
    if code:
        raise SystemExit("Command `%s` exited with code %d" % (cmdstr, code))

def main(args=sys.argv[1:]):

    # parse command line arguments
    parser = OptionParser('%prog [options] location')
    parser.add_option('-m', '--message', dest='message',
                      help='commit message')
    parser.add_option('-u', '--remote-url', dest='remote_url',
                      default="http://k0s.org/hg/",
                      help="URL of host hg repository collection [Default: %default]")
    parser.add_options('-p', '--remote-path', dest='remote_path',
                       help="remote path of hg repository links; otherwise taken from --remote-url, if specified")
    options, args = parser.parse_args(args)
    if len(args) != 1:
        parser.print_usage()
        parser.exit()
    # TODO: sanity check for remote_url, remote_path

    # setup repository
    name = os.path.basename(directory)
    call(['hg', 'init'])
    call(['hg', 'add'])
    call(['hg', 'commit', '-m', options.message or 'initial commit of %s' %name])

    # setup remote, if specified
    if options.remote_url:

        # parse remote URL
        host, netloc, path, query, anchor = urlparse.urlsplit(options.remote_url)
        if options.remote_path:
            remote_host = host
            if ':' in remote_path:
                remote_host, remote_path = remote_path.split(':', 1)
        else:
            remote_path = path

        # setup remote repository
        call(['ssh', HOST, "cd %s/%s && hg init && hg add && hg ci -m '%s'" % (repo, name, options.message or 'initial commit of %s' % name)])

        # write local .hgrc file
        # TODO: use ConfigParser
        f = file(os.path.join('.hg', 'hgrc'), 'w')
        print >> f, HGRC % { 'host': HOST, 'repo': repo, 'name': name}

if __name__ == '__main__':
  main()
