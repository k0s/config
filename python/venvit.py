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

import sys

# class for VCS
# TODO: hg, git, ...

# usage

args = sys.argv[1:]
if len(args) != 1:
    print "Usage: %prog <svn-or-hg-location>"


# determine name of the package
NAME=
for i in /trunk /branches /tag
do
    NAME=${NAME%%$i*}
done
NAME=${NAME%%/} # remove trailing slash
NAME=${NAME##*/}

if svn info $1 2> /dev/null
then
    CHECKOUT="svn co"
else
    CHECKOUT="hg clone"
fi

# create a virtualenv and install the software
VIRTUAL_ENV_LOCATION="${HOME}/virtualenv/virtualenv.py"
python ${VIRTUAL_ENV_LOCATION} ${NAME}
cd ${NAME}
source bin/activate
mkdir src/
cd src/
$CHECKOUT $1 ${NAME}
cd ${NAME}
python setup.py develop
