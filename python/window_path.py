#!/usr/bin/env python

import os
import subprocess
import sys
import window_title

def main(filename):
    title = window_title.active_window_title()
    path = os.path.expanduser(title)
    if not os.path.exists(path):
        return
    path = os.path.abspath(path)
    return os.path.join(path, filename)

if __name__ == '__main__':
    print main(sys.stdin.read().strip())
