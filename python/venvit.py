#!/usr/bin/env python
"""
venvit.py -- the equivalent of ez_setup.py for virtualenv, but less intrusive;
It wants a one-step installation to install python into a new virtualenv.
venvit is meant to be used via e.g. curl, although you can download it as well:

 curl http://example.com/path/to/venvit.py | python - <package>

If <package> is a package name, it tries to install it from the cheeseshop.

If it is a svn/hg/git/tgz/etc URL, it should download and install the software
in source.

Only useful output -- like the scripts installed -- should be output to the
user.

Ideally, packages could have a venvit__init__.py (or a better name) that
will be executed after installation (or a venvit.txt which would just be output
to console, maybe falling back to the README
"""
