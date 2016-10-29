#!/usr/bin/env python

import datadiff
import optparse
import sys
import yaml

def main(args=sys.argv[1:]):
    usage = '%prog [options] from.yml to.yml'
    parser = optparse.OptionParser(usage=usage)
    options, args = parser.parse_args()
    if len(args) != 2:
        parser.error("Please supply two .yml files")

    # compare the output
    output0 = yaml.load(file(args[0]))
    output1 = yaml.load(file(args[1]))
    diff = datadiff.diff(output0, output1, context=1, fromfile=args[0], tofile=args[1])
    print diff

if __name__ == '__main__':
    main()
