#!/usr/bin/env python

"""
get the active window title
"""

import re
import subprocess

def active_window_id():
    process = subprocess.Popen(['xprop', '-root'], stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    for line in stdout.splitlines():
        if '_NET_ACTIVE_WINDOW(WINDOW):' in line:
            return line.rsplit(None, 1)[-1]

def window_title(window_id):
    process = subprocess.Popen(['xprop', '-id', window_id], stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    for line in stdout.splitlines():
        match = re.match("WM_NAME\((?P<type>.+)\) = (?P<name>.+)", line)
        if match:
            type = match.group("type")
            if type == "STRING" or type == "COMPOUND_TEXT":
                return match.group("name").strip('"')

def active_window_title():
    return window_title(active_window_id())

def main():
    title = active_window_title()
    print title

if __name__ == '__main__':
    main()
