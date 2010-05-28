#!/bin/bash

YOUTUBEDL=/home/jhammel/music/youtube-dl

URL=$1
TITLE=$($YOUTUBEDL --get-title $URL)
EXT=mp4
$YOUTUBEDL -b -i -r 50k $URL -o "%(title)s.${EXT}" 
rm -f audiodump.wav
mplayer -vc null -vo null -ao pcm "$TITLE.$EXT"
lame -q 2 audiodump.wav "$TITLE.mp3"
#rm "$TITLE.$EXT"