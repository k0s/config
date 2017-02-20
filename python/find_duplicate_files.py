#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
find duplicate files in a directory
"""

# imports
import argparse
import csv
import difflib
import json
import os
import sys


class DuplicateFilesParser(argparse.ArgumentParser):
    """CLI option parser"""

    def __init__(self, **kwargs):
        kwargs.setdefault('description', __doc__)
        argparse.ArgumentParser.__init__(self, **kwargs)
        self.add_argument('directory')
        self.add_argument('--identical-sizes', dest='identical_sizes',
                          action='store_true', default=False,
                          help="print out all matches with identical sizes and exit")
        self.options = None

    def parse_args(self, *args, **kw):
        options = argparse.ArgumentParser.parse_args(self, *args, **kw)
        self.validate(options)
        self.options = options
        return options

    def validate(self, options):
        """validate options"""
        if not os.path.isdir(options.directory):
            self.error("Not a directory: {}".format(options.directory))


def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line options
    parser = DuplicateFilesParser()
    options = parser.parse_args(args)

    # get all file sizes
    sizes = {}
    directory = options.directory
    for dirpath, dirnames, files in os.walk(directory, topdown=True):
        for path in files:
            path = os.path.join(dirpath, path)
            sizes.setdefault(os.path.getsize(path), []).append(path)

    # filter out those with identical sizes
    identical_sizes = {k: v for k, v in sizes.items()
                       if len(v) > 1}
    if options.identical_sizes:
        print(json.dumps(identical_sizes, indent=2, sort_keys=True))


    # now that we've narrowed it down, let's find the identical files
    duplicate_files = []
    for row in identical_sizes.values():

        while len(row) > 1:
            duplicates = []
            ref_file = row.pop()
            ref = open(ref_file).read()
            for index, path in reversed(list(enumerate(row))):
                comp = open(path).read()
                if ref == comp:
                    if not duplicates:
                        duplicates.append(ref_file)
                    duplicates.append(path)
                    row.pop(index)
            if duplicates:
                duplicate_files.append(duplicates)


    # output CSV
    writer = csv.writer(sys.stdout)
    writer.writerows(duplicate_files)

if __name__ == '__main__':
    main()
