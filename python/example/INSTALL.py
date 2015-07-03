#!/usr/bin/env python

"""
install and setup stuff
"""

### imports
import argparse
import inspect
import os
import subprocess
import sys

### globals
string = (str, unicode)
BASEDIR = os.environ.get('VIRTUAL_ENV', os.getcwd())

def comment(text, comment_character='#', join=False):
    """
    comment some text

    text -- text to comment
    join -- whether to ``str.join`` the lines of text
    """
    text = text.strip()
    if text:
        retval = ['{} {}'.format(comment_character, line.rstrip())
                  for line in text.splitlines()]
    else:
        retval = []
    if join:
        retval =  '\n'.join(retval)
    return retval


class Command(object):
    """an individual command"""
    def __init__(self, command):
        self.command = command
    def shell(self):
        return isinstance(self.command, string)
    def interpolate(self, **variables):
        if self.shell():
            return self.command.format(**variables)
        return [i.format(**variables) for i in self.command]
    def commandline(self, **variables):
        command = self.interpolate(**variables)
        if self.shell():
            return command
        else:
            return subprocess.list2cmdline(command)
    __str__ = commandline
    def __call__(self, variables=None, **kwargs):
        variables = variables or {}
        commandline = self.commandline(**variables)
        kwargs['shell'] = self.shell()
        print (commandline)
        code = subprocess.call(self.interpolate(**variables), **kwargs)
        if code:
            raise subprocess.CalledProcessError(code, commandline)


### setup and installation steps

class Step(object):
    commands = []
    env = {}
    comment_character = '#'

    @classmethod
    def name(cls):
        return cls.__name__
    @classmethod
    def description(cls):
        return (getattr(cls, '__doc__', '') or '').strip()
    @classmethod
    def name_and_description(cls):
        description = cls.description()
        return '{}{}'.format(cls.name(), ': {}'.format(description if description else ''))
    def __init__(self, **variables):
        self.commands = self.commands[:]
        self.variables = variables
        for key in self.env:
            os.environ[key] = self.env[key].format(**variables)
    def command_objs(self):
        return [Command(command) for command in self.commands]
    def interpolate(self):
        return [command.interpolate(**self.variables)
                for command in self.command_objs()]
    def write(self, output=sys.stdout):
        for command in self.command_objs():
            output.write(str(command) + '\n')
    def __call__(self):
        for command in self.command_objs():
            command(variables=self.variables)
    def script(self):
        retval = comment(self.name(), self.comment_character)
        description = self.description()
        if description:
            retval.extend(comment(description, self.comment_character))
        for command in self.command_objs():
            retval.append(command.commandline(**self.variables))
        return '\n'.join(retval)

class UbuntuPackages(Step):
    commands = [['sudo', 'apt-get', '-y', 'update'],
                ['sudo', 'apt-get', '-y', 'upgrade'],
                ]
    packages = []
    def __init__(self, **kwargs):
        Step.__init__(self, **kwargs)
        self.commands.append(['sudo', 'apt-get', '-y', 'install'] + self.packages)

class InstallXinePrerequisites(UbuntuPackages):
    """install the prerequisites for the xine-based client"""
    packages = ['libcurl4-gnutls-dev',
                'g++',
                'libx11-dev',
                'libxext-dev',
                'libxine1',
                'libxine-dev',
                'gxine',
                ]

class InstallFFMPEG(UbuntuPackages):
    """install prerequisites for the FFMPEG-based client"""
    packages = ['subversion',
                'make',
                'gcc',
                'g++',
                'libcurl4-gnutls-dev']
    yasm = '1.2.0'
    ffmpeg = '1.2'
    def __init__(self, client=os.path.join(BASEDIR, 'linux_client')):
        UbuntuPackages.__init__(self, client=client, yasm=self.yasm, ffmpeg=self.ffmpeg)

        self.commands.extend([['mkdir', '-p', '{client}'],
                              ['wget', 'http://www.tortall.net/projects/yasm/releases/yasm-{yasm}.tar.gz', '-O', '{client}/yasm-{yasm}.tar.gz'],
                              ['wget', 'http://ffmpeg.org/releases/ffmpeg-{ffmpeg}.tar.gz', '-O', '{client}/ffmpeg-{ffmpeg}.tar.gz'],
                              ['tar', 'zfvx', '{client}/yasm-{yasm}.tar.gz', '-C', '{client}'],
                              ['tar', 'zfvx', '{client}/ffmpeg-{ffmpeg}.tar.gz', '-C', '{client}'],

                              # YASM
                              'cd {client}/yasm-{yasm} && ./configure',
                              'cd {client}/yasm-{yasm} && make',
                              'cd {client}/yasm-{yasm} && sudo make install',

                              # FFMPEG
                              'cd {client}/ffmpeg-{ffmpeg} && ./configure --enable-shared',
                              'cd {client}/ffmpeg-{ffmpeg} && make',
                              'cd {client}/ffmpeg-{ffmpeg} && sudo make install',
                              ])


### functionality for running multiple steps

class Steps(object):
    """run a series of steps"""

    comment_character = '#'

    # instance defaults
    defaults = {}

    # variable descriptions
    descriptions = dict()

    def __init__(self, *steps, **variables):
        self.steps = steps
        self.variables = variables
        self.step_dict = {step.name():step for step in steps}

    def parser(self, description=None):
        """return argument parser"""
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('--list', dest='list_steps',
                            action='store_true', default=False,
                            help="list available steps and exit")
        parser.add_argument('--commands', dest='list_commands',
                            action='store_true', default=False,
                            help="list commands to be run and exit")
        return parser

    def comment(self, text, join=False):
        """
        comment some text

        text -- text to comment
        join -- whether to ``str.join`` the lines of text
        """
        return comment(text, self.comment_character, join)

    def script(self, steps=None, description=None, variables=None):
        """returns a script"""
        variables = variables or {}
        retval = ['#!/bin/bash', '']
        if description:
            retval.extend(self.comment(description))
            retval.append('') # whitespace delimiter
        steps = self.instantiate(*steps, **variables)
        for step in steps:
            retval.append(step.script())
            retval.append('') # whitespace

        return '\n'.join(retval)

    @staticmethod
    def args(step):
        args, varargs, varkw, defaults = inspect.getargspec(step.__init__)
        return args[1:]

    def all_args(self, steps=None):
        retval = []
        steps = steps or self.steps
        for step in steps:
            args = self.args(step)
            retval.extend([arg for arg in args if arg not in retval])
        return retval

    def get_variables(self, options, steps=None):
        """get variables from a namespace"""
        return {i:getattr(options, i, None) or self.defaults.get(i)
                for i in self.all_args(steps)}

    def instantiate(self, *steps, **variables):
        """instantiate a set of steps with variables"""
        return [step(**{arg:variables.get(arg)
                        for arg in self.args(step)})
                for step in steps]

    def parse(self, args=sys.argv[1:], description=None):

        # create a parser
        parser = self.parser(description)

        # add step names as arguments
        parser.add_argument('steps', nargs='*', metavar='step',
                            help="steps to run; if omitted, all steps will be run")

        # add step arguments
        for arg in self.all_args():
            variable_description = self.descriptions.get(arg)
            default = self.defaults.get(arg)
            if variable_description and default:
                variable_description += ' [DEFAULT: %(default)s]'
            parser.add_argument('--{}'.format(arg), dest=arg,
                                default=default, help=variable_description)

        # parse arguments
        options = parser.parse_args(args)

        # get steps to run
        if options.steps:
            missing = [i for i in options.steps if i not in self.step_dict]
            if missing:
                parser.error("No such step: {}".format(', '.join(missing)))
            steps = [self.step_dict[i] for i in options.steps]
        else:
            steps = self.steps[:]

        # get variables for execution
        variables = self.get_variables(options)

        if options.list_steps:
            # list steps and exit
            for step in steps:
                print (step.name_and_description())
                variables = self.args(step)
                if variables:
                    print ('Variables: {}'.format(', '.join(variables)))
                print ('') # whitespace
            sys.exit(0)

        # instantiate steps
        step_objs = self.instantiate(*steps, **variables)

        if options.list_commands:
            # print commands and exit
            print (self.script(steps, description, variables))
            sys.exit(0)

        # run steps
        for step in step_objs:
            step()


### main

def main(args=sys.argv[1:]):
    """CLI"""
    Steps(*[InstallXinePrerequisites,
            InstallFFMPEG]).parse(args=args, description=__doc__)

if __name__ == '__main__':
    main()
