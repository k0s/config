#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
serve DLNA
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from which import which

here = os.path.dirname(os.path.realpath(__file__))
string = (str, unicode)

def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name', dest='name', default='protest servant',
                        help="friendly name")
    parser.add_argument('--db-dir', dest='db_dir',
                        default=os.path.join(os.environ['HOME'], 'minidlna'),
                        help='db directory')
    parser.add_argument('-p', '--port', dest='port', default=8200, type=int,
                        help="port")
    parser.add_argument('-v', '--videos', dest='videos', nargs='+',
                        help="videos")
    parser.add_argument('audio', nargs='+')
    parser.add_argument('--print', '--print-config', dest='print_config',
                        action='store_true', default=False,
                        help="write config to stdout and exit")
    options = parser.parse_args(args)

    # dlna location
    dlna = which('minidlnad')
    if not dlna:
        parser.error("minidlna command not found")

    lines = [('friendly_name', options.name),
             ('db_dir', options.db_dir),
             ('log_dir', options.db_dir),
             ('inotify', 'yes'),
             ('enable_tivo', 'yes')]
    lines.extend([('media_dir', 'A,{}'.format(os.path.abspath(d)))
                  for d in options.audio])
    lines.extend([('media_dir', 'V,{}'.format(os.path.abspath(d)))
                  for d in options.audio])
    config = '\n'.join(['{}={}'.format(*line) for line in lines])
    print (config)

    if options.print_config:
        parser.exit()

    fd, name = tempfile.mkstemp()
    os.write(fd, config)
    os.close(fd)

    command = [dlna, '-f', name, '-p', str(options.port)]
    print (subprocess.list2cmdline(command))
    subprocess.check_call(command)

    os.remove(name)
    shutil.rmtree(options.db_dir)

if __name__ == '__main__':
    main()
