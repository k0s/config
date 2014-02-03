#!/usr/bin/env python

"""
multiprocessing/subprocess experiments
"""

import argparse
import os
import subprocess # http://bugs.python.org/issue1731717
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

        # reset output buffer location
        self.output_buffer.seek(0)

        # set end time
        self.end = time.time()

    def poll(self, process_output=None):

        if process_output is not None:
            self.read(process_output) # read from output buffer
        poll = subprocess.Popen.poll(self)
        if poll is not None:
            self._finalize(process_output)
        return poll

    def wait(self, maxtime=None, sleep=1., process_output=None):
        """
        maxtime -- timeout in seconds
        sleep -- number of seconds to sleep between polling
        """
        while self.poll(process_output) is None:

            # check for timeout
            curr_time = time.time()
            run_time = self.runtime()
            if maxtime is not None and run_time > maxtime:
                self.kill()
                self._finalize(process_output)
                return

            # naptime
            if sleep:
                time.sleep(sleep)

        # finalize
        self._finalize(process_output)

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
            return time.time() - self.start
        return self.end - self.start


def main(args=sys.argv[1:]):
    """CLI"""

    description = """demonstration of how to do things with subprocess"""

    # available programs
    progs = {'yes': ["yes"],
             'ping': ['ping', 'google.com']}

    # parse command line
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-t", "--time", dest="time",
                        type=float, default=4.,
                        help="seconds to run for (or <= 0 for forever)")
    parser.add_argument("-s", "--sleep", dest="sleep",
                        type=float, default=1.,
                        help="sleep this number of seconds between polling")
    parser.add_argument("-p", "--prog", dest='program',
                        choices=progs.keys(), default='ping',
                        help="subprocess to run")
    parser.add_argument("--list-programs", dest='list_programs',
                        action='store_true', default=False,
                        help="list available programs")
    parser.add_argument("--wait", dest='wait',
                        action='store_true', default=False,
                        help="run with ``.wait()`` and a callback")
    parser.add_argument("--callback", dest='callback',
                        action='store_true', default=False,
                        help="run with polling and a callback")
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

    # demo function for processing output
    def output_processor(output):
        print ('[{}]:\n{}\n{}'.format(proc.runtime(),
                                      output.upper(),
                                      '-==-'*10))
    if options.callback:
        process_output = output_processor
    else:
        process_output = None

    if options.wait:
        # wait for being done
        proc.wait(maxtime=options.time, sleep=options.sleep, process_output=output_processor)
    else:
        # start the main subprocess loop
        while proc.poll(process_output) is None:

            if options.time > 0 and proc.runtime() > options.time:
                proc.kill()

            if options.sleep:
                time.sleep(options.sleep)

            if process_output is None:
                # process the output with ``.read()`` call
                read = proc.read()
                output_processor(read)

    # correctness tests
    assert proc.end is not None

    # print summary
    output = proc.output
    n_lines = len(output.splitlines())
    print ("{}: {} lines, ran for {} seconds".format(subprocess.list2cmdline(prog), n_lines, proc.runtime()))

if __name__ == '__main__':
    main()
