#!/usr/bin/env python

import sys
import urllib2
import urllib
content = sys.stdin.read()
url = 'http://pastebin.com/api_public.php'
data = dict(paste_code=content, paste_subdomain='mozilla')
values = urllib.urlencode(data)
req = urllib2.Request(url, values)
response = urllib2.urlopen(req)
the_page = response.read()

print the_page
