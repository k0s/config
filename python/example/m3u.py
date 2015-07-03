#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
m3u playlist manipulator

See:
- https://pypi.python.org/pypi/m3u8
- http://gonze.com/playlists/playlist-format-survey.html#M3U
- http://www.assistanttools.com/articles/m3u_playlist_format.shtml
- http://en.wikipedia.org/wiki/M3U
- http://tools.ietf.org/html/draft-pantos-http-live-streaming-08#section-3.3.1
"""

# imports
import argparse
import m3u8
import os
import subprocess
import sys

# module globals
__all__ = ['main', 'M3UParser']
here = os.path.dirname(os.path.realpath(__file__))
string = (str, unicode)

class Playlist(object):
    def __init__(self, playlists=(), base_path=None):
        self.clips = []
        for playlist in playlists:
            assert os.path.isfile(playlist)
            _base_path = os.path.abspath(base_path or os.path.dirname(os.path.abspath(playlist))) # TODO: this doesn't fix URLs
            content = open(playlist).read()
            m3u = m3u8.M3U8(content, base_path=_base_path)
            for segment in m3u.segments:
                path = segment.uri
                title = segment.title
                self.clips.append((title, path))

    def __str__(self):
        retval = []
        for title, path in self.clips:
            if title:
                line = '{} # {}'.format(os.path.abspath(path), title)
            else:
                line = os.path.abspath(path)
            retval.append(line)
        return '\n'.join(retval)

class M3UParser(argparse.ArgumentParser):
    """CLI option parser"""
    def __init__(self, **kwargs):
        kwargs.setdefault('description', __doc__)
        argparse.ArgumentParser.__init__(self, **kwargs)
        self.add_argument('playlists', metavar='playlist', nargs='+',
                          help="playlist to parse")
        self.add_argument('-b', '--base', dest='base_path', default=os.getcwd(),
                          help="base path [DEFAULT: %(default)s]")
        self.options = None

    def parse_args(self, *args, **kw):
        options = argparse.ArgumentParser.parse_args(self, *args, **kw)
        self.validate(options)
        self.options = options
        return options

    def validate(self, options):
        """validate options"""
        if not os.path.exists(options.base_path):
            self.error("Base path '{}' does not exist".format(options.base_path))
        missing = [i for i in options.playlists
                   if not os.path.exists(i)]
        if missing:
            self.error("Playlist not found: {}".format(', '.join(missing)))

def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line options
    parser = M3UParser()
    options = parser.parse_args(args)

    # create playlist
    playlist = Playlist(options.playlists, options.base_path)

    # print out some things
    print ('{}'.format(playlist))

if __name__ == '__main__':
    main()
