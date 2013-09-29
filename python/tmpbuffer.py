#!/usr/bin/env python

# from http://k0s.org/hg/bitsyblog/file/5c04cf601aba/bitsyblog/blogme.py

import optparse
import os
import subprocess
import tempfile

def tmpbuffer(editor=None):
    """open an editor and retreive the resulting editted buffer"""

    if not editor:
        editor = os.environ.get('EDITOR')
        if not editor:
            raise Exception("tmpbuffer: editor not supplied and EDITOR not defined")
    tmpfile = tempfile.mktemp(suffix='.txt')
    cmdline = editor.split() # XXX shlex would be more powerful
    cmdline.append(tmpfile)
    edit = subprocess.call(cmdline)
    buffer = file(tmpfile).read().strip()
    os.remove(tmpfile)
    return buffer

if __name__ == '__main__':
    # purely for testing/illustration purposes
    contents = tmpbuffer()
    print contents

