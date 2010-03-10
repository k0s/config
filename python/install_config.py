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
    commands = [ ['virtualenv/virtualenv.py', package],
                 ['mkdir', '%s/src'],
                 ['hg', 'clone', src, '%s/src/%s' % (package, package)],
                 ['%s/bin/python', '%s/src/%s/setup.py', 'develop'] ]
    execute(*commands)

# install some python
install_develop('smartopen')

postinstall_commands = [ ['ln', '-s', os.path.join(HOME, 'smartopen', 'bin', 'smartopen'), os.path.join(HOME, 'bin', 'smartopen')]
