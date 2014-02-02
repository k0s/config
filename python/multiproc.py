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
    defaults = {'bufsize': 1, # line buffered
                'store_output': True, # store stdout
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
        self.location = 0
        self.output_buffer = tempfile.SpooledTemporaryFile()
        self.output = '' if _kwargs.pop('store_output') else None
        _kwargs['stdout'] = self.output_buffer

        # runtime
        self.start = time.time()
        self.end = None

        # launch subprocess
        subprocess.Popen.__init__(self, command, **_kwargs)

    def _finalize(self, process_output):
        """internal function to finalize"""

        # read final output
        self.read(process_output)

        # reset output buffer
        self.output_buffer.seek(0)

        # set end time
        self.end = time.time()

    def wait(self, maxtime=None, sleep=1., process_output=None):
        """
        maxtime -- timeout in seconds
        sleep -- number of seconds to sleep between polling
        """
        while self.poll() is None:

            # check for timeout
            curr_time = time.time()
            run_time = curr_time - self.start
            if run_time > maxtime:
                self.kill()
                self._finalize(process_output)
                return

            # read from output buffer
            self.read(process_output)

            # naptime
            if sleep:
                time.sleep(sleep)

        # finalize
        self._finalize()

        return self.returncode # set by ``.poll()``

    def read(self, process_output=None):
        """read from the output buffer"""

        self.output_buffer.seek(self.location)
        read = self.output_buffer.read()
        if self.output is not None:
            self.output += read
        if process_output:
            process_output(read)
        self.location += len(read)
        return read

    def commandline(self):
        """returns string of command line"""

        if isinstance(self.command, string):
            return self.command
        return subprocess.list2cmdline(self.command)

    __str__ = commandline

    def runtime(self):
        """returns time spent running or total runtime if completed"""

        if self.end is None:
            return self.end - self.start
        return time.time() - self.start


def main(args=sys.argv[1:]):
    """CLI"""

    # available programs
    progs = {'yes': ["yes"],
             'ping': ['ping', 'google.com']}

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
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
        sys.exit(0)

    # select program
    prog = progs[options.program]

    # start process
    proc = Process(prog)

    # callback for output processing
    def process_output(output):
        print output.upper()

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

    # wait for being done
    proc.wait(maxtime=options.time, sleep=options.sleep, process_output=process_output)

    # finalization
    output = proc.output
    n_lines = len(output.splitlines())
    print ("{}: {} lines".format(subprocess.list2cmdline(prog), n_lines))

if __name__ == '__main__':
    main()
