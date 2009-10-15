#!/usr/bin/env python
import os

# make sure duplicate path elements aren't printed twice
def ordered_set(alist):
    seen = set()
    new = []
    for item in alist:
        if item in seen:
            continue
        seen.add(item)
        new.append(item)
    return new

def lsex(path=None):
    """
    list executable files on the path
    o path: list of directories to search.  if not specified, use system path
    """

    if path is None:
        # use system path
        path = ordered_set(os.environ['PATH'].split(':'))

    executables = []

    # add the executable files to the list
    for i in path:
        if not os.path.isdir(i):
            continue
        files = [ os.path.join(i,j) for j in os.listdir(i) ]
        files = filter(lambda x: os.access(x, os.X_OK), files)
        files.sort() # just to make the output pretty
        executables.extend(files)
    return executables

if __name__ == '__main__':
    for i in lsex():
        print i
