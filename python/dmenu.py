#!/usr/bin/env python

import optparse
import os
import subprocess
import sys

def choose_file(directory, dmenu='dmenu'):
    """choose a file in the directory with dmenu"""
    directory = os.path.abspath(directory)
    files = os.listdir(directory)
    string = '\n'.join(files)


    process = subprocess.Popen([dmenu, '-i'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = process.communicate(input=string)
    if process.returncode:
        return
    chosen = os.path.join(directory, stdout)
    if os.path.isdir(chosen):
        return choose_file(chosen)
    return chosen

def main(args=sys.argv[1:]):
    parser = optparse.OptionParser()
    print choose_file(os.getcwd())

if __name__ == '__main__':
    main()
