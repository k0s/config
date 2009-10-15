
SSCONVERT=`which ssconvert 2> /dev/null`;
if [ -z "${SSCONVERT}" ]; then
    echo "${SSCONVERT} not found.  Please install gnumeric.";
    return 1;
fi;
for i in "$@";
do
    OUTPUT=${i%.xls}.txt;
    $SSCONVERT -I Gnumeric_Excel:excel -T Gnumeric_stf:stf_csv "$i" "$OUTPUT" 2>/dev/null;
    cat "$OUTPUT";
done


