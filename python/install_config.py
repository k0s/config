#!/usr/bin/env python
"""
installs config to a user's home directory
this can be done with
curl http://k0s.org/hg/config/python/install-config.py | python
"""

SRC='http://k0s.org/hg/config'
import os
os.chdir(os.environ['HOME'])

# make the current directory a repository
import subprocess
subprocess.check_call(['hg', 'init'])
subprocess.check_call(['hg', 'pull', SRC])
subprocess.check_call(['hg', 'update', '-C'])


