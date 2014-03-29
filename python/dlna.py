#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import sys
import tempfile
from which import which

here = os.path.dirname(os.path.realpath(__file__))
string = (str, unicode)

def main(args=sys.argv[1:]):

    dlna = which('minidlna')
    assert dlna

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name', dest='name', default='protest servant',
                        help="friendly name")
    parser.add_argument('--db-dir', dest='db_dir',
                        default=os.path.join(os.environ['HOME'], 'minidlna'),
                        help='db directory')
    parser.add_argument('-p', '--port', dest='port', default=8200, type=int,
                        help="port")
    parser.add_argument('audio', nargs='+')
    options = parser.parse_args(args)

    lines = [('friendly_name', options.name),
             ('db_dir', options.db_dir),
             ('log_dir', options.db_dir),
             ('inotify', 'yes'),
             ('enable_tivo', 'yes')]
    lines.extend([('media_dir', 'A,{}'.format(os.path.abspath(d)))
                  for d in options.audio])
    config = '\n'.join(['{}={}'.format(*line) for line in lines])
    print (config)

    fd, name = tempfile.mkstemp()
    os.write(fd, config)
    os.close(fd)

    command = [dlna, '-f', name, '-d', '-p', str(options.port)]
    print (subprocess.list2cmdline(command))
    subprocess.check_call(command)

    os.remove(name)

if __name__ == '__main__':
    main()
