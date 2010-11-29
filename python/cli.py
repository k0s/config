#!/usr/bin/env python

"""
program illustrating command line in the form of
``--option foo`` or ``--option=foo`` goes to a (key,value) paid
and ``-tag`` gets appended to a list.  Further options go to a further list::

    >>> main(['-foo', '--bar=fleem', 'baz'])
    (['foo'], {'bar': 'fleem'}, ['baz'])
"""

import sys

class ParserError(Exception):
  """error for exceptions while parsing the command line"""

def main(_args=sys.argv[1:]):

  # return values
  _dict = {}
  tags = []
  args = []

  # parse the arguments
  key = None
  for arg in _args:
    if arg.startswith('---'):
      raise ParserError("arguments should start with '-' or '--' only")
    elif arg.startswith('--'):
      if key:
        raise ParserError("Key %s still open" % key)
      key = arg[2:]
      if '=' in key:
        key, value = key.split('=', 1)
        _dict[key] = value
        key = None
        continue
    elif arg.startswith('-'):
      if key:
        raise ParserError("Key %s still open" % key)
      tags.append(arg[1:])
      continue
    else:
      if key:
        _dict[key] = arg
        continue
      args.append(arg)

  # return values
  return (_dict, tags, args)

if __name__ == '__main__':
  _dict, tags, args = main()
  print _dict
  print tags
  print args
