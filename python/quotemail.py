#!/usr/bin/env python

"""
quote as per email
"""
# TODO -> textshaper

def prefix(text, quote='> '):
    return '\n'.join(['%s%s' % (quote, line.rstrip())
                      for line in text.strip().splitlines()])

if __name__ == '__main__':
    import sys
    import optparse
    usage = '%prog [options] [file] <file2> <...>'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-i', '--in-place', dest='in_place',
                      action='store_true', default=False,
                      help="")
    options, args = parser.parse_args()
    if args:
        for arg in args:
            with file(arg) as f:
                contents = f.read()
            quoted = prefix(contents)
            if options.in_place:
                with file(arg, 'w') as f:
                    f.write(quoted)
            else:
                print quoted
    else:
        print prefix(sys.stdin.read())
