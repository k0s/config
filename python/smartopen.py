#!/usr/bin/python

""" smart open the data passed in """

import urllib
import urllib2
import sys
import os
import address

class Location:
    """
    generic class for locations
    """

    def __init__(self, baseurl=""):
        self.baseurl = baseurl

    def url(self, query):
        return self.baseurl + self.process(query)

    def process(self, query):
        return query

    def test(self, query):
        return True

    def open(self, query):
        if not self.test(query):
            return False
        url = self.url(query)
        os.system("firefox '%s'" % url)
        return True

class URL(Location):
    """a straight URL"""

    def process(self, query):
        if '://' in query:
            return query
        return 'http://' + query

    def test(self, query):
        """try to open the url"""

        if ' ' in query or '\n' in query:
            return False

        try:
            site = urllib.urlopen(self.process(query))
        except IOError:
            return False
        return True

class GoogleMap(Location):
    """try to google-maps the address"""

    def __init__(self):
        gmapsurl='http://maps.google.com/maps?f=q&hl=en&q='
        Location.__init__(self, gmapsurl)

    def process(self, query):
        theaddress = address.normalizeaddress(query)
        if not theaddress:
            return theaddress
        return urllib.quote_plus(theaddress)

    def test(self, query):
        return bool(self.process(query))

class Revision(Location):
    def __init__(self):
        revision_url = 'http://trac.openplans.org/openplans/changeset/'
        Location.__init__(self, revision_url)

    def process(self, query):
        return query[1:]

    def test(self, query):
        if query[0] != 'r':
            return False
        return query[1:].isdigit()
            
        

class TracTicket(Location):
    def __init__(self):
        # url for # data
        number_url = 'http://trac.openplans.org/openplans/ticket/'
        Location.__init__(self, number_url)

    def process(self, query):
        if query.startswith('#'):
            return query[1:]        
        return query

    def test(self, query):
        query = self.process(query)
        if len(query.split()) != 1:
            return False
        return query.isdigit()

class Wikipedia(Location):
    """try to open the query in wikipedia"""
    def __init__(self):        
        wikiurl = 'http://en.wikipedia.org/wiki/'
        Location.__init__(self, wikiurl)

    def process(self, query):
        return urllib.quote_plus('_'.join(query.split()))
        
    def test(self, query):
        'test to see if the article exists'

        # need a phony user agent so wikipedia won't know we're a bot
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.0.4) Gecko/20060508 Firefox/1.5.0.4'
        
        request = urllib2.Request(self.url(query), None, headers)
        f = urllib2.urlopen(request).read()

        if 'Wikipedia does not have an article with this exact name' in f:
            return False
        return True

class Google(Location):
    def __init__(self):        
        googleurl = 'http://www.google.com/search?hl=en&q='
        Location.__init__(self, googleurl)
        
    def process(self, query):
        return urllib.quote_plus(query)

# get data to be operated on
data = ' '.join(sys.argv[1:])
if not data:
    data = sys.stdin.read()

locations = [ URL, 
              GoogleMap,
              Revision,
              TracTicket,
              Wikipedia,
              Google
              ]

for loc in locations:
    loc = loc()
    if loc.open(data):
        sys.exit(0)
