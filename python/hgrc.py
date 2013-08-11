#!/usr/bin/env python

"""
Script for modifying hgrc files.

If no arguments specified, the repository given by `hg root` is used.
"""

# imports
import optparse
import os
import subprocess
import sys
import urlparse
from ConfigParser import RawConfigParser as ConfigParser

class section(object):
    def __init__(self, function, section_name, *section_names):
        self.function = function
        self.sections = [section_name]
        self.sections.extend(section_names)
    def __call__(self, parser):
        import pdb; pdb.set_trace()

#@parser # decorator makes this x-form path -> ConfigParser automagically
@section('paths')
def set_default(parser, default):
    """set [paths]:default"""

def set_default_push(parser, default_push):
    """
    set [paths]:default-push to `default_push`
    """
    if 'paths' not in parser.sections():
        parser.add_section('paths')
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
    parser.add_option('--default', dest='default',
                      help="set [paths] default entry")
    parser.add_option('-p', '--print', dest='print_ini',
                      action='store_true', default=False,
                      help="print .ini contents")
    options, args = parser.parse_args(args)

    # sanitization
    if options.default_push and options.default_push_ssh:
        parser.error("Cannot set --push and --ssh")

    # if not specified, use repo from `hg root`
    if not args:
        args = [subprocess.check_output(['hg', 'root']).strip()]

    # if not specified, set a default action
    default_action = 'default_push_ssh'
    available_actions = ('default_push',
                        'default_push_ssh',
                        'list_hgrc',
                        )
    actions = dict([(name, getattr(options, name))
                    for name in available_actions
                    if getattr(options, name)])
    if not actions:
        actions = {'default_push_ssh': True}

    # find all hgrc files
    hgrc = []
    missing = []
    not_hg = []
    not_a_directory = []
    errors = {'Missing path': missing,
              'Not a mercurial directory': not_hg,
              'Not a directory': not_a_directory,
              }
    for path in args:
        if not os.path.exists(path):
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
                print '%s: %s' % (key, ', '.join(value))
        parser.exit(1)

    # construct ConfigParser objects and
    # ensure that all the files are parseable
    config = {}
    for path in hgrc:
        config[path] = ConfigParser()
        if isinstance(path, basestring):
            if os.path.exists(path):
                config[path].read(path)

    # print the chosen hgrc paths
    if actions.pop('list_hgrc', None):
        print '\n'.join(hgrc)

    # map of actions -> functions;
    # XXX this is pretty improv; to be improved
    action_map = {'default_push_ssh': set_default_push_to_ssh,
                  'default_push': set_default_push
                  }

    # alter .hgrc files
    action_names = actions.keys()
    while actions:

        # XXX crappy
        action_name = action_names.pop()
        parameter = actions.pop(action_name)
        method = action_map[action_name]
        if action_name == 'default_push_ssh':
            parameter = None

        # apply to all files
        for path, ini in config.items():
            if parameter is not None:
                method(ini, parameter)
            else:
                method(ini)

    # print .hgrc files, if specified
    for path, ini in config.items():
        print '+++ %s' % (path)
        ini.write(sys.stdout)
        print

if __name__ == '__main__':
    main()
