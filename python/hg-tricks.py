"""
random collection of hg tricks in python
"""

# XXX STUB

from subprocess import check_output as call

### check status

def changes(hg='hg')
    """check for outstanding changes"""
    output = call([hg, 'st']).strip()
    lines = [line for line in output.splitlines()
             if not line.startswith('?')]
    if lines:
        print "Outstanding changes:"
        print output
        return True

