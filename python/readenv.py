#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
parse environment variables
"""

import argparse
import os
import subprocess
import sys

def parse_env(output):
    return dict([line.split('=',1) for line in output.splitlines()])

def read_env(script):
    """read environment following source script"""
    command = 'bash -c "(. {} &> /dev/null) && /usr/bin/env"'.format(script)
    command = "(. {} &> /dev/null) && /usr/bin/env".format(script)
    output = subprocess.check_output(command, shell=True, env={})
    return parse_env(output)

def diff_env(script):
    before = parse_env(subprocess.check_output('/usr/bin/env', shell=True))
    after = read_env(script)


if __name__ == '__main__':
    """test"""

    import tempfile
    from pprint import pprint

    example = """export FOO=bar
export FLEEM=foobar"""


    fd, name = tempfile.mkstemp()
    os.write(fd, example)
    os.close(fd)
    print (open(name).read())

    pprint(name)
    pprint(read_env(name))
