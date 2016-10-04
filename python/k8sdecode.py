#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
get a kubernetes secret and decode it
"""

# imports
import argparse
import base64
import json
import os
import subprocess
import sys


def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('secret',
                        help="k8s secret name")
    options = parser.parse_args(args)

    # get JSON from `kubectl`
    command = ['kubectl', 'get', 'secret', options.secret, '-o', 'json']
    try:
        output = subprocess.check_output(command)
    except subprocess.CalledProcessError as e:
        print (e)
        sys.exit(e.returncode)
    data = json.loads(output)['data']

    # decode them
    output = {key: base64.b64decode(value)
              for key, value in data.items()}

    # output them
    print (json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
