#!/usr/bin/env python

"""
illustrates usage of the undefined pattern from e.g.
http://k0s.org/mozilla/hg/bzconsole/file/tip/bzconsole/command.py

This is useful for scenarios similar to:
- you have base configuration in a file
- you have an OptionParser to read options in the command line
- the CLI options should overwrite the file configuration iff
  the user specifies an option
"""

from optparse import OptionParser

class Undefined(object):
    def __init__(self, default):
        self.default=default

class UndefinedOptionParser(OptionParser):

    def add_option(self, *args, **kwargs):
        kwargs['default'] = Undefined(kwargs.get('default'))
        OptionParser.add_option(self, *args, **kwargs)

    def parse_args(self, *args, **kwargs):
        options, args = OptionParser.parse_args(self, *args, **kwargs)
        return options, args

if __name__ == '__main__':

    myparser = UndefinedOptionParser()
    myparser.add_option("--foo", dest='foo', default='hello')
    myparser.add_option("--bar", dest='bar', default='goodbye')
    myparser.add_option("--baz", dest='baz', default='helloagain')
    myparser.add_option("--fleem", dest='fleem', default='aufwiedersehen')

    myconfiguration = {'foo': 'hi',
                       'bar': 'ciao'}
    options, args = myparser.parse_args(['--foo', 'hello', '--baz', 'hola'])
    for key, value in options.__dict__.items():
        # XXX ideally you would move this to parse_args
        if isinstance(value, Undefined):
            options.__dict__[key] = myconfiguration.get(key, value.default)

    assert options.foo == 'hello'
    assert options.bar == 'ciao'
    assert options.baz == 'hola'
    assert options.fleem == 'aufwiedersehen'
