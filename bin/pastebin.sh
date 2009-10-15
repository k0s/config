# all spaces must be converted to '+'
# all newlines must be converted to %0D%0A
# this is probably better off converted in a python script

CONTENT_DATA=`python -c "import sys; print '%0D%0A'.join(sys.stdin.read().split('\n'))" | sed 's/ /+/g'`

#echo $CONTENT_DATA
#CONTENT_DATA=`echo ${CONTENT_DATA} | sed 's/ /+/g'`
#echo $CONTENT_DATA
#CONTENT_DATA=`echo ${CONTENT_DATA} | sed 's/$/%0D%0A/g'`

wget --post-data="content=${CONTENT_DATA}&s=Submit+Post&description=&type=1&expiry=&name=" -O- http://www.pastebin.ca/index.php | grep 'meta http-equiv="refresh"' | sed 's/^.*\(http:[^"]*\).*/\1/'

