#!/bin/bash

# illustrate self-writing script (example)
# This one does something hard and replaces dynamic data with sed.
# Other solutions (magic markers, etc) are possible

path=`readlink -f $0`
mode=`stat --format '%a' ${path}`
tmp=`tempfile --mode ${mode}`
datestamp=`date`
nonce="This script last generated at "

# sanity check
if [[ ! -w "${path}" ]]
then
    echo "You don't have write permission for script ${path}"
    exit 1
fi

# avoiding -i for safety
sed 's/\(echo \"'"${nonce}"'\).*\"/\1'"${datestamp}"'\"/' ${path} > ${tmp}
if [[ ! -e "${tmp}" ]]
then
    echo "Temporary file creation not successful"
    exit 1
fi

# echo last and current generation times for example
echo "This script last generated at Sat Jun  8 08:52:05 PDT 2013"
echo "Now: ${datestamp}"

# move tmpfile -> script location via exec
exec mv ${tmp} ${path}
