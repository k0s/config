#!/usr/bin/env python
"""
installs config to a user's home directory
this can be done with
curl http://k0s.org/hg/config/raw-file/tip/python/install_config.py | python
"""

SRC='http://k0s.org/hg/config'
import os
import sys
HOME=os.environ['HOME']
os.chdir(HOME)

# make the current directory a repository
import subprocess

commands = [ ['hg', 'init'],
             ['hg', 'pull', SRC],
             ['hg', 'update', '-C'],
             ['hg', 'clone', 'http://bitbucket.org/ianb/virtualenv'],

             # site-specific files
             ['mkdir', '-p', '.subversion'],
             ['rm', '-f', '.subversion/config'],
             ['ln', '-s', os.path.join(HOME, '.subversion_config/config'), os.path.join(HOME, '.subversion/config')],
             ]

def execute(*commands):
    for command in commands:
        print ' '.join(command)
        code = subprocess.call(command)
        if code:
            sys.exit(code)

execute(*commands)

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

postinstall_commands = [ ['ln', '-s', os.path.join(HOME, 'smartopen', 'bin', 'smartopen'), os.path.join(HOME, 'bin', 'smartopen') ] ]

execute(*postinstall_commands)

# TODO:
# - ubuntu packages to install:
PACKAGES="unison fluxbox antiword xclip"
print "Ensure the following packages are installed:"
print "sudo apt-get install $PACKAGES"
