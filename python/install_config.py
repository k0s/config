#!/usr/bin/env python
"""
installs config to a user's home directory
this can be done with
curl http://k0s.org/hg/config/raw/tip/python/install_config.py | python
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

             # site-specific files
             ['rm', '.subversion/config'],
             ['ln', '-s', os.path.join(HOME, '.subversion_config/config'), os.path.join(HOME, '.subversion/config')],
             ]

for command in commands:
    code = subprocess.call(command)
    if code:
        sys.exit(code)



