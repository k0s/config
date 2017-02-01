#!/usr/bin/env python

import psutil

PSNAME = 'python'

for process in psutil.process_iter():
    try:
        memory = process.memory_info()
        if process.name() == PSNAME:
            print int(memory.rss)
    except Exception:
        pass
