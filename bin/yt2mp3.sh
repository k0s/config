#!/bin/bash

YOUTUBEDL=/home/jhammel/music/youtube-dl

URL=$1
TITLE=$($YOUTUBEDL --get-title $URL)
$YOUTUBEDL -b -i -r 50k $URL -o "%(title)s.%(ext)s" 
EXT=mp4
rm -f audiodump.wav
mplayer -vc null -vo null -ao pcm "$TITLE.$EXT"
lame -q 2 audiodump.wav "$TITLE.mp3"
rm "$TITLE.$EXT"