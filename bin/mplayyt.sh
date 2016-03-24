#!/bin/bash

# curl "$(youtube-dl --get-url https://www.youtube.com/watch?v=LI9hJf27JLY | head -n 1)" | mplayer -cache 1024 -

for URL in $@
do
    curl "$(youtube-dl --get-url $URL | head -n 1)" | mplayer -cache 1024 -
done