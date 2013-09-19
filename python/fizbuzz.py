#!/usr/bin/env python

for i in range(1,101):
    print ''.join([label for val, label in ((3, 'Fizz'), (5, 'Buzz'))
                   if not i % val]) or i
