#!/usr/bin/python

"""
make a virtualenv for the product
"""

import sys

# class for VCS
# TODO: hg, git, ...

# usage

args = sys.argv[1:]
if len(args) != 1:
    print "Usage: %prog <svn-or-hg-location>"
fi

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
