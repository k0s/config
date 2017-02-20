#!/usr/bin/env python

"""
Script for modifying hgrc files.

If no arguments specified, the repository given by `hg root` is used.

If http(s):// arguments are given, create hgrc file from such a thing
"""

## TODO:
#  - functionality to populate [web]-> description in hgrc file from
#    setup.py, e.g.
#    http://stackoverflow.com/questions/1541778/mercurial-how-do-i-populate-repository-descriptions-for-hgwebdir-cgi
#    Could also loop over a directory; e.g.
#    `hgrc --setup-web . # loop over all .hg repos in this directory`

# imports
import optparse
import os
import subprocess
import sys
from collections import OrderedDict
from ConfigParser import RawConfigParser as ConfigParser
from StringIO import StringIO

try:
    # python 2
    import urlparse
except ImportError:
    import urllib.parse as urlparse

### global methods

def isHTTP(path):
    """is path an {http,https}:// URL?"""
    return urlparse.urlsplit(path)[0] in ('http', 'https')

class section(object):
    def __init__(self, section_name, *section_names):
        self.sections = [section_name]
        self.sections.extend(section_names)
    def __call__(self, function):
        def wrapped(parser, *args, **kwargs):
            for section in self.sections:
                if section not in parser.sections():
                    parser.add_section(section)
            function(parser, *args, **kwargs)
        return wrapped


@section('paths')
def set_default(parser, default):
    """set [paths]:default"""
    parser.set('paths', 'default', default)

@section('paths')
def set_default_push(parser, default_push):
    """
    set [paths]:default-push to `default_push`
    """
    parser.set('paths', 'default-push', default_push)

def set_default_push_to_ssh(parser):
    """
    set `[paths]:default-push` to that given by `[paths]:default` but
    turn the protocol to 'ssh'
    If `[paths]:default` is not there, do nothing.
    Returns True if written, otherwise False
    """

    # get [paths]:default value
    if 'paths' not in parser.sections():
        return False
    if not parser.has_option('paths', 'default'):
        return False
    default = parser.get('paths', 'default')

    # parse URL
    scheme, netloc, path, query, anchor = urlparse.urlsplit(default)
    ssh_url = urlparse.urlunsplit(('ssh', netloc, path, query, anchor))

    # set
    set_default_push(parser, ssh_url)
    return True # XXX could instead be url to set to or old value


def main(args=sys.argv[1:]):

    # parse command line arguments
    usage = '%prog [options] repository <repository> <...>'
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    parser.add_option('-l', '--list', dest='list_hgrc',
                      action='store_true', default=False,
                      help="list full path to hgrc files")
    parser.add_option('--ssh', dest='default_push_ssh',
                      action='store_true', default=False,
                      help="use `default` entries for `default-push`")
    parser.add_option('--push', '--default-push', dest='default_push',
                      help="set [paths] default-push location")
    parser.add_option('-d', '--default', dest='default',
                      help="set [paths] default entry")
    parser.add_option('-p', '--print', dest='print_ini',
                      action='store_true', default=False,
                      help="print .ini contents")
    parser.add_option('--dry-run', dest='dry_run',
                      action='store_true', default=False,
                      help="don't write to disk")
    options, args = parser.parse_args(args)

    # sanitization
    if options.default_push and options.default_push_ssh:
        parser.error("Cannot set --push and --ssh")

    # if not specified, use repo from `hg root`
    if not args:
        args = [subprocess.check_output(['hg', 'root']).strip()]

    # if not specified, set a default action
    default_action = 'default_push_ssh'
    available_actions = ('default',
                         'default_push',
                         'default_push_ssh',
                         'print_ini',
                         'list_hgrc',
                        )
    actions = [(name, getattr(options, name))
               for name in available_actions
               if getattr(options, name)]
    if not actions:
        # add a default action for our convenience
        actions = [('default_push_ssh', True)]
    actions = OrderedDict(actions)
    if not actions:
        parser.error("Please specify an action")

    # find all hgrc files and URLs
    hgrc = []
    missing = []
    not_hg = []
    not_a_directory = []
    urls = []
    errors = {'Missing path': missing,
              'Not a mercurial directory': not_hg,
              'Not a directory': not_a_directory,
              }
    for path in args:
        if not os.path.exists(path):
            if isHTTP(path):
                hgrc.append(path)
                urls.append(path)
                continue
            missing.append(path)
        path = os.path.abspath(os.path.normpath(path))
        if os.path.isdir(path):
            basename = os.path.basename(path)
            subhgdir = os.path.join(path, '.hg') # hypothetical .hg subdirectory
            if basename == '.hg':
                hgrcpath = os.path.join(path, 'hgrc')
            elif os.path.exists(subhgdir):
                if not os.path.isdir(subhgdir):
                    not_a_directory.append(subhgdir)
                    continue
                hgrcpath = os.path.join(subhgdir, 'hgrc')
            else:
                not_hg.append(path)
                continue
            hgrc.append(hgrcpath)
        else:
            assert os.path.isfile(path), "%s is not a file, exiting" % path
            hgrc.append(path)

    # raise errors if encountered
    if filter(None, errors.values()):
        for key, value in errors.items():
            if value:
                print ('%s: %s' % (key, ', '.join(value)))
        parser.exit(1)

    # construct ConfigParser objects and
    # ensure that all the files are parseable
    config = {}
    for path in hgrc:
        config[path] = ConfigParser()
        if isinstance(path, basestring):
            if os.path.exists(path):
                config[path].read(path)
            elif path in urls:
                if 'default' not in actions:
                    set_default(config[path], path)

    # print the chosen hgrc paths
    if 'list_hgrc' in actions:
        print ('\n'.join(hgrc))

        # remove from actions list
        actions.pop('list_hgrc', None)

    # map of actions -> functions;
    # XXX this is pretty improv; to be improved
    action_map = {'default_push_ssh': set_default_push_to_ssh,
                  'default_push': set_default_push,
                  'default': set_default
                  }

    # cache for later (XXX)
    print_ini = actions.pop('print_ini', bool(urls))

    # alter .hgrc files
    for action_name, parameter in actions.items():

        # XXX crappy
        method = action_map[action_name]
        if action_name == 'default_push_ssh':
            parameter = None

        # apply to all files
        for path, ini in config.items():

            # call method with parser
            if parameter is None:
                method(ini)
            else:
                method(ini, parameter)

    # print .hgrc files, if specified
    if print_ini:
        values = []
        for path, ini in config.items():
            _buffer = StringIO()
            ini.write(_buffer)
            value = _buffer.getvalue().strip()
            if len(config) == 1:
                values = [value]
            else:
                values.append('+++ %s\n%s' % (path, value))
        print ('\n'.join(values))

    # write .ini files
    for path, ini in config.items():
        if path in urls:
            continue
        with open(path, 'w') as f:
            ini.write(f)

if __name__ == '__main__':
    main()
