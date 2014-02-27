#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import os
import subprocess
import sys
import time

def main(args=sys.argv[1:]):

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('seconds_since_epoch', help="seconds since epoch input")
    options = parser.parse_args(args)

    

if __name__ == '__main__':
    main()
