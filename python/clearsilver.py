#!/usr/bin/python

import sys, os

KEY_RETURN="""
"""

class ClearSilver(object):
    """
    a blatant rip-off of quicksilver/katapult
    """
    def __init__(self, startswith=''):
        self.matches = {}
        self.sortable = True
        if startswith:
            self.build_matches(startswith)

    def returnmatch(self):
        keys = self.matches.keys()
        if len(keys) == 1:
            return keys[0], self.matches[keys[0]]
        if self.sortable:
            keys.sort()
        return keys

    def find_matches(self, startswith):
        nixlist = []
        for i in self.matches:
            if not i.startswith(startswith):
                nixlist.append(i)

        for i in nixlist:
            self.matches.pop(i)
            
        return self.returnmatch()
        

class PATHsilver(ClearSilver):    

    def build_matches(self, startswith=''):
        path = os.environ['PATH'].split(':')
        path.reverse()
        for directory in path:
            try:
                for binary in os.listdir(directory):
                    if binary.startswith(startswith):
                        self.matches[binary] = '/'.join((directory,binary))
            except OSError:  # directory not found
                continue
        return self.returnmatch()


    def exec_match(self, key):
        item = self.matches[key]
        os.execl(item, item)
      

class Wordsilver(ClearSilver):
    dictfile = '/usr/share/dict/cracklib-small'
    
    def build_matches(self, startswith=''):
        f = file(self.dictfile, 'r')
        for i in f.readlines():
            if i.startswith(startswith):
                i = i.rstrip('\r\n')
                self.matches[i] = i
        return self.returnmatch()

    def exec_match(self, key):        
        item = self.matches[key]
        print key

class BookmarkSilver(ClearSilver):
    def __init__(self, startswith=''):
        ClearSilver.__init__(self)
        self.sortable = False
        if startswith:
            self.build_matches(startswith)
            
    def add_url(self, i, startswith):
        delimiter = '//'
        j = i[i.index(delimiter) + len(delimiter):]
        j = j.rstrip('/')
        if j.startswith(startswith):
            self.matches[j] = i
            j = j.strip('w.')
        if j.startswith(startswith):
            self.matches[j] = i
            
    def build_matches(self, startswith=''):
        # find the firefox files
        firefoxdir = '/'.join((os.environ['HOME'], '.mozilla', 'firefox'))
        profile = file('/'.join((firefoxdir, 'profiles.ini')), 'r').readlines()
        profile = [i.rstrip('\n\r \t')  for i in profile]
        index = profile.index('Name=default')
        delimiter = 'Path='
        while 1:
            index += 1
            if profile[index].startswith(delimiter):
                profile = '/'.join((firefoxdir, profile[index][len(delimiter):]))
                break
        bookmarks = '/'.join((profile, 'bookmarks.html'))
        history = '/'.join((profile, 'history.dat'))
        import re
        history = file(history, 'r').read()
        history = re.findall('http.*//.*\)', history)
        history.reverse()
        for i in history:
            i = i[:i.index(')')]
            self.add_url(i, startswith)

        bookmarks = file(bookmarks, 'r').read()
        bookmarks = re.findall('"http.*//.*"', bookmarks)

        for i in bookmarks:
            i = i.strip('"')
            i = i[:i.index('"')]
            self.add_url(i, startswith)

        return self.returnmatch()

    def exec_match(self, key):
        item = self.matches[key]
        
        os.system("firefox " + item)

if __name__ == '__main__':

    matcher_type = 'PATHsilver'

    # parse options
    options = { 'D' : 'Wordsilver', 'H' : 'BookmarkSilver' }
    for i in sys.argv[1:]:
        i = i.strip('-')
        if options.has_key(i):
            matcher_type = options[i]

    # init the 'GUI'
    import curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)

    try:
# XXX should include colors at some point -- not right now, though
#        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

        c = ''
        matcher = None
        matches = None
        entered=''
        
        while 1:
            y, x = stdscr.getmaxyx()
            stdscr.refresh()
            c = stdscr.getch()
            stdscr.erase()

            # handle backspaces 
            if c == curses.KEY_BACKSPACE or c == 127:
                entered = entered[:-1]
                matcher = None
                matches = None
            else:
                
                try:
                    c = chr(c)
                except ValueError:
                    continue
                
                if c == KEY_RETURN:
                    break
            
                entered += c
                
            if not matcher:
                matcher = eval(matcher_type + "()")
                matches = matcher.build_matches(entered)
            else:
                
                if c.isdigit() and int(c) < min(10, len(matches)):        
                    for i in matches:
                        if i.startswith(entered):
                            break
                    else:
                        matches = matches[int(c):int(c)+1]
                        break

                matches = matcher.find_matches(entered)

                
            if isinstance(matches, list):
                i=1
                for match in matches:
                    if i >= y: continue
                    if i <= 10:
                        numstr = " :" + str(i-1)
                    else:
                        numstr = ""
                    stdscr.addstr(i,0, match + numstr)
                    i += 1
                stdscr.addstr(0,0, entered)

                if matches: stdscr.addstr(1,0, matches[0] + " :0")
            else:
                stdscr.addstr(0,0,entered + " -> " + matches[1])

    finally:
        # 'GUI' cleanup
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()
        
        # execute the program (if found)
        if not matches:
            sys.exit(1)
        matcher.exec_match(matches[0])
                    
    
