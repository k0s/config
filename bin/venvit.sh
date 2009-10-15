#!/bin/bash

if (( $# != 1 ))
then
    echo "Usage: $0 <svn-location>"
    exit 0
fi

NAME=$1

for i in /trunk /branches /tag
do
    NAME=${NAME%%$i*}
done
NAME=${NAME##*/}

#echo $NAME

VIRTUAL_ENV_LOCATION="${HOME}/virtualenv/virtualenv.py"

python ${VIRTUAL_ENV_LOCATION} ${NAME}
cd ${NAME}
source bin/activate
mkdir src/
cd src/
svn co $1 ${NAME}
cd ${NAME}
python setup.py develop
