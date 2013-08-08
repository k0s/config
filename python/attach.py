#!/usr/bin/env python

"""
attach strace to a process:

624  sudo strace -p $(pidof firefox)
625  kill 6976
626  isrunning firefox

Optionally kill the process when detached
"""


import optparse
import os
import subprocess
import sys

from subprocess import check_output

def main(args=sys.argv[1:]):

    usage = '%prog [options] ProgramName_or_PID'
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    parser.add_option('-k', '--kill',
                      action='store_true', default=False,
                      help="kill process after strace is done")
    options, args = parser.parse_args(args)
    if len(args) != 1:
        parser.print_usage()
        parser.error("Please specify program or PID to attach to")

    # get the PID
    try:
        pid = int(args[0])
    except ValueError:
        pid = check_output(["pidof", args[0]]).strip().split()
        if len(pid) > 1:
            parser.error("Multiple PIDs found for %s:\n%s" % (args[0],
                                                              '\n'.join(pid)))
        # TODO: handle not matching case
        pid = int(pid[0])

    # invoke strace
    subprocess.call(['sudo', 'strace', '-p', str(pid)])

    # kill if specified
    os.kill(pid, 9) # TODO: better than SIGKILL

if __name__ == '__main__':
    main()
