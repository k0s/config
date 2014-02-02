#!/usr/bin/env python

"""
multiprocessing/subprocess experiments
"""

import argparse
import os
import subprocess
import sys
import time
import tempfile

string = (str, unicode)

class Process(subprocess.Popen):
    """why would you name a subprocess object Popen?"""

    # http://docs.python.org/2/library/subprocess.html#popen-constructor
    defaults = {'buffsize': 1, # line buffered
                }

    def __init__(self, command, **kwargs):

        # setup arguments
        self.command = command
        _kwargs = self.defaults.copy()
        _kwargs.update(kwargs)

        # on unix, ``shell={True|False}`` should always come from the
        # type of command (string or list)
        if not subprocess.mswindows:
            _kwargs['shell'] = isinstance(command, string)

        # output buffer
        self.output_buffer = tempfile.SpooledTemporaryFile()
        self.location = 0
        self.output = []
        _kwargs['stdout'] = self.output_buffer

        # launch subprocess
        self.start = time.time()
        subprocess.Popen.__init__(self, command, **_kwargs)

    def wait(self, maxtime=None, sleep=1.):
        """
        maxtime -- timeout in seconds
        sleep -- number of seconds to sleep between polling
        """
        while self.poll() is None:

            # check for timeout
            curr_time = time.time()
            run_time = curr_time - self.start
            if run_time > maxtime:
                # TODO: read from output
                return process.kill()

            # read from output buffer
            self.output_buffer.seek(self.location)
            read = self.output_buffer.read()
            self.location += len(read)

            # naptime
            if sleep:
                time.sleep(sleep)

        # reset tempfile
        output.seek(0)

        return self.returncode # set by ``.poll()``

    def commandline(self):
        """returns string of command line"""

        if isinstance(self.command, string):
            return self.command
        return subprocess.list2cmdline(self.command)

    __str__ = commandline


def main(args=sys.argv[1:]):
    """CLI"""

    # available programs
    progs = {'yes': ["yes"],
             'ping': ['ping', 'google.com']}


    # parse command line
    usage = '%prog [options]'
    parser = argparse.ArgumentParser(usage=usage, description=__doc__)
    parser.add_argument("-t", "--time", dest="time",
                        type=float, default=4.,
                        help="seconds to run for")
    parser.add_argument("-s", "--sleep", dest="sleep",
                        type=float, default=1.,
                        help="sleep this number of seconds between polling")
    parser.add_argument("-p", "--prog", dest='program',
                        choices=progs.keys(), default='ping',
                        help="subprocess to run")
    parser.add_argument("--list-programs", dest='list_programs',
                        action='store_true', default=False,
                        help="list available programs")
    options = parser.parse_args(args)

    # list programs
    if options.list_programs:
        for key in sorted(progs.keys()):
            print ('{}: {}'.format(key, subprocess.list2cmdline(progs[key])))

    # select program
    prog = progs[options.program]

    proc = Process(prog)

    # # start the main subprocess loop
    # # TODO -> OO
    # output = tempfile.SpooledTemporaryFile()
    # start = time.time()
    # proc = subprocess.Popen(prog, stdout=output)
    # location = 0
    # while proc.poll() is None:
    #     curr_time = time.time()
    #     run_time = curr_time - start
    #     if run_time > options.time:
    #         proc.kill()
    #     output.seek(location)
    #     read = output.read()
    #     location += len(read)
    #     print ('[{}] {}\n{}'.format(run_time, read, '-==-'*10))
    #     if options.sleep:
    #         time.sleep(options.sleep)

    # # reset tempfile
    # output.seek(0)

    n_lines = len(output.read().splitlines())
    print ("{}: {} lines".format(subprocess.list2cmdline(prog), n_lines))

if __name__ == '__main__':
    main()
