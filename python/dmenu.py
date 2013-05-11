#!/usr/bin/env python

import optparse
import os
import subprocess
import sys

def choose_file(directory, dmenu='dmenu',
                args=('-i', '-nb', 'black', '-nf', 'white')):
    """choose a file in the directory with dmenu"""
    directory = os.path.abspath(directory)
    files = os.listdir(directory)
    string = '\n'.join(files)

    if isinstance(dmenu, basestring):
        dmenu = [dmenu]
    dmenu = list(dmenu)
    dmenu.extend(args)

    process = subprocess.Popen(dmenu, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = process.communicate(input=string)
    if process.returncode:
        return
    chosen = os.path.join(directory, stdout)
    if os.path.isdir(chosen):
        return choose_file(chosen)
    return chosen

def main(args=sys.argv[1:]):
    parser = optparse.OptionParser()
    parser.add_option('-d', '--directory', dest='directory',
                      default=os.getcwd(),
                      help="call on this directory [Default: current directory]")
    parser.add_option('-e', '--exec', dest='executable',
                      help="call this proram with the result")
    options, args = parser.parse_args(args)
    chosen =  choose_file(options.directory)
    if chosen:
        if options.executable:
            pass
        print chosen
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
