#!/usr/bin/env python
"""
installs config to a user's home directory
this can be done with
curl http://k0s.org/hg/config/raw-file/tip/python/install_config.py | python
"""

SRC='http://k0s.org/hg/config'
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

             # get virtual env
             ['hg', 'clone', 'http://bitbucket.org/ianb/virtualenv'],
             ['ln' '-s', HOME + '/virtualenv/virtualenv.py', HOME + '/bin/'],

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

# make a (correct) .hg/hgrc file for $HOME
subprocess.call('/bin/echo -e "[paths]\\ndefault = http://k0s.org/hg/config\\ndefault-push = ssh://k0s.org/hg/config" > ~/.hg/hgrc', shell=True)

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
    
# install some python
install_develop('smartopen')
install_develop('silvermirror') # XXX this won't actually work since python-dev isn't installed; install it first

postinstall_commands = [ ['ln', '-s', os.path.join(HOME, 'smartopen', 'bin', 'smartopen'), os.path.join(HOME, 'bin', 'smartopen') ],
                         ['ln', '-s', os.path.join(HOME, 'silvermirror', 'bin', 'silvermirror'), os.path.join(HOME, 'bin', 'silvermirror') ],
                         ]
execute(*postinstall_commands)


# - ubuntu packages to install:
PACKAGES="unison fluxbox antiword xclip graphviz python-dev python-lxml"
print "Ensure the following packages are installed:"
print "sudo apt-get install $PACKAGES"
