#!/usr/bin/env python

# https://stackoverflow.com/questions/473620/how-do-you-create-a-daemon-in-python

"""
POST /
{
 "command": ["", ...]
 "cwd": ""
 "env: {"": ""}
}
->
200 OK
{
  "pid": 123
}

GET /1
{
  "returncode": null # or e.g. 2
  (stdout, stderr)
}
"""

from webob import Request, Response

class WebWaiter:

    def __call__(self, environ, start_response):
        request = Request(environ)
        res = Response(content_type='text/plain')
        res.body = bytes("hello world", "utf-8")
        return res(environ, start_response)


if __name__ == '__main__':
    import argparse
    import wgsiref

    parser = argparse.ArgumentParser(description=__doc__)
    options = parser.parse_args()
