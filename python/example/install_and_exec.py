#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
illustrates installation and execution following installation
"""

import os
import subprocess
import sys

here = os.path.dirname(os.path.realpath(__file__))

try:
    import gnupg
    print ("gnupg installed")
except ImportError:
    print ("gnupg not installed")
    subprocess.check_call(['pip', 'install', 'gnupg'])
    args = [sys.executable] + sys.argv
    os.execl(sys.executable, *args)
