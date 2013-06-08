#!/bin/bash

# illustrate self-writing script (example)
# This one does something hard and replaces dynamic data with sed.
# Other solutions (magic markers, etc) are possible

path=`readlink -f $0`
tmp=`tempfile`
datestamp=`date`
nonce="This script regenerated at "

# avoiding -i for safety
sed 's/\(echo \"'"${nonce}"'\).*\"/\1'"${datestamp}"'\"/' ${path} > ${tmp}

echo "This script regenerated at "