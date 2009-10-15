import random
import sys
import time

from optparse import OptionParser

parser = OptionParser()
parser.add_option('-f', '--file')
parser.add_option('-o', '--output')
(options, args) = parser.parse_args()

if options.file:
    f = file(options.file)    
else:
    f = sys.stdin

lines = [ line.strip() or '\n' for line in f.read().strip().split('\n') ]
content = '\n'.join(lines)
fortunes = [i.strip() for i in content.split('\n\n') ]
f.close()

while 1:
    if options.output:
        f = file(sig, 'w')
        print >> f, random.choice(fortunes)
        f.close()
    else:
        print random.choice(fortunes)
    time.sleep(1)

