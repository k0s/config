#!/usr/bin/env python
"""
installs config to a user's home directory
this can be done with
curl http://k0s.org/hg/config/raw/tip/python/install_config.py | python
"""

SRC='http://k0s.org/hg/config'
import os
import sys
os.chdir(os.environ['HOME'])

# make the current directory a repository
import subprocess

commands = [ ['hg', 'init'],
             ['hg', 'pull', SRC],
             ['hg', 'update', '-C' ] ]

for command in commands:
    code = subprocess.call(command)
    if code:
        sys.exit(code)



