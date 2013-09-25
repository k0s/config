#!/usr/bin/env python

"""
makes a new python project.
"""

import subprocess


- Make or utilize a virutalenv

@requires("makeitso")
- Make a project skeleton:

    makeitso python-project -o ${PROJECT}

- Make a (mercurial) repository:

    hg init .
    hg add
    hg commit -m '${PROJECT}: initial stub'

- Push upstream:

    ssh k0s.org
    cd hg; hg init ${PROJECT}
    exit
    hgrc http://k0s.org/hg/${PROJECT} > .hg/hgrc
    hg push
"""

# see also 
# http://blog.ishans.info/2012/06/10/adding-a-template-for-new-python-files-in-emacs/

import optparse
import sys


def main(args=sys.argv[1:]):
    pass

if __name__ == '__main__':
    main()
