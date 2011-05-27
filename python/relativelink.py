#!/usr/bin/env python

def link(path_info, path=None):

    segments = path_info.split('/')
    if segments[0]:
        segments.insert(0, '')
    
    if len(segments) <3:
        if not path or path == '/':
            return './'
        return path

    nlayers = len(segments[2:])
    string = '../' * nlayers

    if not path or path == '/':
        return string
    return string + path

if __name__ == '__main__':
    import sys
    assert len(sys.argv[1:]) == 2, "need two arguments"
    path_info, path = sys.argv[1:]
    print link(path_info, path)
