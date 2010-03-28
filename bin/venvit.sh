#!/bin/bash
# make a virtualenv for the product

# usage
if (( $# != 1 ))
then
    echo "Usage: $0 <svn-or-hg-location>"
    exit 0
fi

# determine name of the package
NAME=$1
for i in /trunk /branches /tag
do
    NAME=${NAME%%$i*}
done
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
