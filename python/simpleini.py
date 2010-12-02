#!/usr/bin/env python

import os

def read(fp, comments=';#', separators=('=', ':')):

  if isinstance(fp, basestring):
    fp = file(fp)

  sections = []
  key = value = None
  
  for line in fp.readlines():

    stripped = line.strip()

    # ignore blank lines
    if not stripped:
      continue

    # ignore comment lines
    if stripped[0] in comments:
      continue

    # check for a new section
    if len(stripped) > 2 and stripped[0] == '[' and stripped[-1] == ']':
      section = stripped[1:-1].strip()
      sections.append((section, {}))
      key = value = None
      # TODO: should probably make sure this section doesn't already exist
      continue

    # if there aren't any sections yet, something bad happen
    if not sections:
      raise Exception('No sections yet :(')

    # (key, value) pair
    for separator in separators:
      if separator in stripped:
        key, value = stripped.split(separator, 1)
        key = key.strip()
        value = value.strip()
        sections[-1][1][key] = value
        # TODO: should probably make sure this key isn't already in the section
        break
    else:
      # continuation line ?
      if line[0].isspace() and key:
        value = '%s%s%s' % (value, os.linesep, stripped)
        sections[-1][1][key] = value
      else:
        # something bad happen!
        raise Exception("Not sure what you're trying to do")

  return sections

if __name__ == '__main__':
  import sys
  for i in sys.argv[1:]:
    print read(i)
