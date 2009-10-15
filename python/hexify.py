#!/usr/bin/env python
import sys
print ''.join([ '%'+ hex(ord(i))[-2:] for i in ' '.join(sys.argv[1:]) ])
