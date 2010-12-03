#!/usr/bin/env python

import os

def read(fp, variables=None, default='DEFAULT',
         comments=';#', separators=('=', ':'),
         interpolate=True, strict=True):
  """
  read an .ini file and return a list of [(section, values)]
  - fp : file pointer or name to read
  - variables : default set of variables
  - default : name of the section for the default section
  - comments : characters that if they start a line denote a comment
  - separators : strings that denote key, value separation in order
  - strict : whether to be strict about parsing
  """

  if variables is None:
    variables = {}

  if isinstance(fp, basestring):
    fp = file(fp)

  sections = []
  key = value = None
  section_names = set([])

  # read the lines
  for line in fp.readlines():

    stripped = line.strip()

    # ignore blank lines
    if not stripped:
      # XXX should probably reset key and value to avoid continuation lines
      key = value = None
      continue

    # ignore comment lines
    if stripped[0] in comments:
      continue

    # check for a new section
    if len(stripped) > 2 and stripped[0] == '[' and stripped[-1] == ']':
      section = stripped[1:-1].strip()
      key = value = None

      # deal with DEFAULT section
      if section.lower() == default.lower():
        if strict:
          assert default not in section_names
        section_names.add(default)
        current_section = variables
        continue

      if strict:
        # make sure this section doesn't already exist
        assert section not in section_names

      section_names.add(section)

      current_section = {}
      sections.append((section, current_section))
      continue

    # if there aren't any sections yet, something bad happen
    if not section_names:
      raise Exception('No sections yet :(')

    # (key, value) pair
    for separator in separators:
      if separator in stripped:
        key, value = stripped.split(separator, 1)
        key = key.strip()
        value = value.strip()

        if strict:
          # make sure this key isn't already in the section or empty
          assert key
          if current_section is not variables:
            assert key not in current_section
        
        current_section[key] = value
        break
    else:
      # continuation line ?
      if line[0].isspace() and key:
        value = '%s%s%s' % (value, os.linesep, stripped)
        current_section[key] = value
      else:
        # something bad happen!
        raise Exception("Not sure what you're trying to do")

  # interpret the variables
  def interpret_variables(global_dict, local_dict):
    variables = global_dict.copy()
    variables.update(local_dict)

    # string intepolation
    if interpolate:
      nonce = '__s__'
      assert nonce not in global_dict
      global_dict[nonce] = '%s'
      for key, value in variables.items():
        try:
          value = value.replace('%s', '%(__s__)s') % global_dict
          variables[key] = value
        except:
          if strict:
            del global_dict[nonce]
            raise Exception("could not intepolate variable %s: %s" % (key, value))
          pass
          
      del global_dict[nonce]
    return variables

  sections = [(i, interpret_variables(variables, j)) for i, j in sections]
  return sections

if __name__ == '__main__':
  import sys
  for i in sys.argv[1:]:
    path = os.path.abspath(i)
    print read(i, strict=False, variables=dict(here=os.path.dirname(path)))
