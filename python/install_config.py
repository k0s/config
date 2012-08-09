#!/usr/bin/env python

"""
installs config to a user's home directory
this can be done with
curl http://k0s.org/hg/config/raw-file/tip/python/install_config.py | python
"""

SRC='http://k0s.org/hg/config'

import imp
import os
import subprocess
import sys

# go home
HOME=os.environ['HOME']
os.chdir(HOME)

commands = [ # make the home directory a repository
             ['hg', 'init'],
             ['hg', 'pull', SRC],
             ['hg', 'update', '-C'],

             # site-specific files
             ['mkdir', '-p', '.subversion'],
             ['rm', '-f', '.subversion/config'],
             ['ln', '-s', os.path.join(HOME, '.subversion_config/config'), os.path.join(HOME, '.subversion/config')],
             ]

def execute(*commands):
    """execute a series of commands"""
    for command in commands:
        print ' '.join(command)
        code = subprocess.call(command)
        if code:
            sys.exit(code)

execute(*commands)

# get the which command
sys.path.append(os.path.join(HOME, 'python'))
from which import which


# make a (correct) .hg/hgrc file for $HOME
hgrc = """[paths]
default = http://k0s.org/hg/config
default-push = ssh://k0s.org/hg/config
"""
f = file('.hg/hgrc', 'w')
f.write(hgrc)
f.close()

def install_develop(package):
    src = 'http://k0s.org/hg/%s' % package
    directory = '%s/src/%s' % (package, package)
    commands = [ ['virtualenv/virtualenv.py', package],
                 ['mkdir', '-p', directory ],
                 ['hg', 'clone', src, directory] ]
    execute(*commands)
    old_directory = os.getcwd()
    os.chdir(directory)
    command = ['../../bin/python',  'setup.py', 'develop']
    execute(command)
    os.chdir(old_directory)

# do git stuff
git = which('git')
if git:
    # get virtual env
    virtualenv_commands = [['git', 'clone', 'https://github.com/pypa/virtualenv.git'],
                           ['ln', '-s', HOME + '/virtualenv/virtualenv.py', HOME + '/bin/']]
    execute(*virtualenv_commands)

    # setup git's global ignore, since git is silly about this
    # and doesn't look for the file in the right place
    execute(['git', 'config', '--global', 'core.excludesfile', os.path.join(HOME, '.gitignore')])

    # install some python
    install_develop('smartopen')
    install_develop('silvermirror') # XXX this won't actually work since python-dev isn't installed; install it first

    postinstall_commands = [ ['ln', '-s', os.path.join(HOME, 'smartopen', 'bin', 'smartopen'), os.path.join(HOME, 'bin', 'smartopen') ],
                             ['ln', '-s', os.path.join(HOME, 'silvermirror', 'bin', 'silvermirror'), os.path.join(HOME, 'bin', 'silvermirror') ],
                             ]
    execute(*postinstall_commands)
else:
    print "git not installed"

# - ubuntu packages to install:
PACKAGES="mercurial unison fluxbox antiword xclip graphviz python-dev python-lxml curl arandr git emacs"
print "Ensure the following packages are installed:"
print "sudo apt-get install %s" % PACKAGES
