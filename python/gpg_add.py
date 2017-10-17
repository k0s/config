#!/usr/bin/env python

"""
add a line to a gpg file; requires `gpg` on your path
"""

# Reference:
# - https://www.gnupg.org/gph/en/manual/x110.html
# - https://www.gnupg.org/gph/en/manual/x56.html
# - http://tuxlabs.com/?p=450

import argparse
import os
import shutil
import subprocess
import sys
import tempfile


def main(args=sys.argv[1:]):
    """CLI"""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', help="path to GPG file")
    parser.add_argument('line', help='line to add + encrypt')
    options = parser.parse_args(args)

    if not os.path.isfile(options.file):
        parser.error("Not a file: '{}'".format(options.file))

    tmpdir = tempfile.mkdtemp()
    try:
        # decrypt the file
        outfile = os.path.join(tmpdir, options.file + '.decrypted')
        subprocess.check_call(['gpg', '--output', outfile, '--decrypt', options.file])
        assert os.path.exists(outfile)

        # read lines
        with open(outfile) as f:
            lines = f.read().strip().splitlines()

        # write the file
        lines.append(options.line)
        with open(outfile, 'w') as f:
            f.write('\n'.join(lines))

        # encrypt
        subprocess.check_call(['gpg', '--output', options.file, '--symmetric', outfile])
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

if __name__ == '__main__':
    main()
