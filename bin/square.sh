#!/usr/bin/env bash

# crop IN to a centered square SIZExSIZE image, whichever side is shorter

set -euo pipefail

USAGE="$0 IN SIZE OUT"

if [[ "$#" != 3 ]];
then
    echo "$USAGE" >&2
    exit 1
fi

IN=$1
SIZE=$2
OUT=$3

# ^ scales so the *shorter* side is SIZE; -extent then trims the longer side
magick "$IN" -resize "${SIZE}x${SIZE}^" -gravity center -extent "${SIZE}x${SIZE}" "$OUT"
