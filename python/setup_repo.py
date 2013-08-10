#!/usr/bin/env python

"""
setup a repository

Parameters:
- host URL
- location on host disk
"""

# TODO:
# There are patterns here...
# - actions
# - ...

import os
import subprocess
import sys
import urlparse

from optparse import OptionParser

call = subprocess.check_output

def init_repo(directory):
    """setup repository"""
    call(['hg', 'init', directory])
    call(['hg', 'add', '-R', directory])
    call(['hg', 'commit', '-m', options.message, '-R', directory])

def write_hgrc(directory, host, repo, name):
    """write hgrc file"""

    HGRC="""[paths]
default = http://%(host)s/%(repo)s/%(name)s
default-push = ssh://%(host)s/%(repo)s/%(remote_path)s
"""

    path = os.path.join(directory, '.hg', 'hgrc')
    # TODO: use ConfigParser
    with file(os.path.join(directory, '.hg', 'hgrc'), 'w') as f:
        print >> f, HGRC % { 'host': host, 'repo': repo, 'name': name}


def setup_remote(local_repo, remote_url, push='ssh', remote_path=None, name=None):
    """
    setup a remote repository for local_repo
    - remote_url : public (pull) URL for remote repository
    - push : protocol for push
    - remote_path : remote path of hg repository links; otherwise taken from --remote-url, if specified
    """

    # parse remote URL
    host, netloc, path, query, anchor = urlparse.urlsplit(remote_url)
    path = path.rstrip('/')

    # derive name
    if name is None:
        if '/' in path:
            prefix, name = path.rsplit('/', 1)
        else:
            name = path
    assert name

    # get remote path, if specified
    if remote_path:

        # split off remote host and path
        # XXX is a separate host necessary?
        remote_host = host
        if ':' in remote_path:
            remote_host, remote_path = remote_path.split(':', 1)
    else:
        remote_path = path

    # setup remote repository
    remote_dir = '~/%s/%s' % (path.lstrip('/'), name)
    command = ['ssh', host, "mkdir -p %s && cd %s && hg init" % (remote_dir, remote_dir)]
    print command
    #    call(command)


def main(args=sys.argv[1:]):

    # parse command line arguments
    parser = OptionParser('%prog [options] directory')
    parser.add_option('-m', '--message', dest='message',
                      default='initial commit',
                      help='commit message [Default: %default]')
    parser.add_option('-u', '--remote-url', dest='remote_url',
                      default="http://k0s.org/hg/",
                      help="URL of host hg repository collection [Default: %default]")
    parser.add_option('-p', '--remote-path', dest='remote_path',
                      help="remote path of hg repository links; otherwise taken from --remote-url, if specified")
    parser.add_option('-o', '--remote-only', dest='remote_only',
                      action='store_true', default=False,
                      help="setup remote server only")
    options, args = parser.parse_args(args)

    # sanitization
    if not args:
        args = [os.getcwd()]
    if len(args) != 1:
        parser.print_usage()
        parser.exit()
    directory = args[0]

    # initialize repository
    if options.remote_only:
        assert options.remote_url
    else:
        init_repo(directory)

    # setup remote, if specified
    name = os.path.basename(directory)
    if options.remote_url:

        # setup remote repository
        setup_remote(directory, options.remote_url, name=name, remote_path=options.remote_path)

        # push changes
        call(['hg', 'push', '-R', directory])

if __name__ == '__main__':
  main()
