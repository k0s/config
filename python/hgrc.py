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
from ConfigParser import RawConfigParser as ConfigParser

#@parser # decorator makes this x-form path -> ConfigParser automagically
def set_default_push(parser, default_push):
    """
    set [paths]:default_push to `default_push`
    """
    pass

def set_default_push_to_ssh(parser):
    """
    pass
    """

    # get default path
    default = ''

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

        # apply to all files
        for path, ini in config.items():
            if parameter is not None:
                method(ini, parameter)
            else:
                method(ini)


if __name__ == '__main__':
    main()
