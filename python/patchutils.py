
"""
http://k0s.org/blog/20100821174911

Tag -> hg
"""

# XXX stub

import subprocess
import which

def call(*args, **kwargs):
    """"""
    return subprocess.check_output(*args, **kwargs)

class ExecuteCommands(object):

    def __init__(self, *commands, **kwargs):
        self.commands = commands
        self.kwargs = kwargs

    def __call__(self):
        for command in self.commands:
            yield call(command, **self.kwargs)

class lsdiff(ExecuteCommands):
    commands = ['lsdiff']
    def __call__(self):
        output = []
        for retval in ExecuteCommands(self):
            raise NotImplementedError

def hg_root(directory=None):
    directory = directory if directory else os.getcwd()

# CLI

def main(args=sys.argv[1:]):
    parser = optparse.OptionParser()
    options, args = parser.parse_args(args)

    # find the root
    root = hg_root()

    # get the files
    paths = lsdiff(root)

if __name__ == '__main__':
    main()
