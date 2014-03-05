#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
merge master to branch
"""
# TODO: combine with k0s.org/hg/gut

import argparse
import os
import subprocess
import sys
import tempfile
from which import which

class Git(object):
    def branch(self):
        """returns branch you are on"""
        return self.branches()[0]
    def branches(self):
        """return all branches, active first"""
        output = subprocess.check_output(['git', 'branch']).strip()
        lines = sorted(output.splitlines(), key=lambda line: line.startswith('*'), reverse=True)
        return [line.strip('*').strip() for line in lines]

    def diff(self):
        """returns diff between active branch and master"""
        branch = self.branch()
        if branch == 'master':
            raise AssertionError("Cannot be on the master branch")
        merge_base = subprocess.check_output(['git', 'merge-base', 'HEAD', 'master']).strip()
        return subprocess.check_output(['git', 'diff', merge_base])

    def checkout(self, branch):
        subprocess.check_output(['git', 'checkout', branch])

    def pull(self, branch='master'):
        current_branch = self.branch()
        if current_branch != branch:
            self.checkout(branch)
        subprocess.check_output(['git', 'pull', 'origin', branch])
        if current_branch != branch:
            self.checkout(current_branch)

    def merge(self):
        pass

def main(args=sys.argv[1:]):

    parser = argparse.ArgumentParser(description=__doc__)
    options = parser.parse_args(args)

    # find branch
    git = Git()
    print (git.diff())


if __name__ == '__main__':
    main()
