#!/usr/bin/env python

import os
import subprocess
import sys

from optparse import OptionParser

HOST='k0s.org'
HGRC="""[paths]
default = http://%(host)s/%(repo)s/%(name)s
default-push = ssh://%(host)s/%(repo)s/%(name)s
"""

def call(command, *args, **kw):
  code = subprocess.call(command, *args, **kw)
  if isinstance(command, basestring):
    cmdstr = command
  else:
    cmdstr = ' '.join(command)
  print cmdstr
  if code:
    raise SystemExit("Command `%s` exited with code %d" % (cmdstr, code))
        
def main(args=sys.argv[1:]):

  parser = OptionParser('%prog [options] location')
  parser.add_option('-m', '--message',
                    help='commit message')
  options, args = parser.parse_args(args)
  
  if len(args) != 1:
    parser.print_usage()
    parser.exit()

  repo = args[0].strip('/')
  
  directory = os.getcwd()
  name = os.path.basename(directory)
  os.chdir('..')
  call(['scp', '-r', name, '%s:~/%s/' % (HOST, repo)])
  call(['ssh', HOST, "cd %s/%s && hg init && hg add && hg ci -m '%s'" % (repo, name, options.message or 'initial commit of %s' % name)])
  os.chdir(directory)
  call(['hg', 'init'])
  call(['hg', 'pull', 'http://%s/%s/%s' % (HOST, repo, name)])
  call(['hg', 'update', '-C'])
  f = file(os.path.join('.hg', 'hgrc'), 'a')
  print >> f, HGRC % { 'host': HOST, 'repo': repo, 'name': name}

if __name__ == '__main__':
  main()
