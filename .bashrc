source /etc/profile

# Test for an interactive shell.  There is no need to set anything
# past this point for scp and rcp, and it's important to refrain from
# outputting anything in those cases.
if [[ $- != *i* ]] ; then
	# Shell is non-interactive.  Be done now!
	return
fi

# Enable colors for ls, etc.  Prefer ~/.dir_colors #64489
if [[ -f ~/.dir_colors ]] ; then
	eval $(dircolors -b ~/.dir_colors)
elif [[ -f /etc/DIR_COLORS ]] ; then
	eval $(dircolors -b /etc/DIR_COLORS)
fi

# variables
export CLICOLOR=1
export EDITOR='emacs -nw'
export MOZCONFIG=~/mozilla/mozconfig
export MOZSOURCE=~/mozilla/src/mozilla-central
export MOZOBJ=~/mozilla/src/obj-browser
export JS_EDITLINE=1

# aliases
alias ls='ls --color=auto'
alias grep='grep --colour=auto'
alias wget='wget --no-check-certificate'
alias datestamp='date +%Y%m%d%H%M%S'
alias zfilt='grep -v "eprecat" | grep -v "ERROR Zope"'
alias svnst='svn st | grep -v "^\?"'
alias awd="python -c 'import os;  print os.path.realpath(\".\")'"
alias distribute='python setup.py egg_info -RDb "" sdist register upload'
alias random="python -c 'import sys, random; foo = sys.argv[1:]; random.shuffle(foo); print \" \".join(foo)'"
alias xpcshell="LD_LIBRARY_PATH=${MOZOBJ}/dist/bin ${MOZOBJ}/dist/bin/xpcshell"

# PROMPT
PS1='> '
PS2='. '
PROMPT_COMMAND='echo -ne "\033]0;${SSH_CLIENT/*/$HOSTNAME:}${PWD/~/~}\007"'

# PATHs
export PATH=~/bin:~/python:$PATH:/usr/sbin:/usr/games/bin
export PYTHONPATH=~/python:$PYTHONPATH


### functions

cdwin() {
# change directory to a window's location using its title
    DIR=$(xwininfo | dictify.py xwininfo | awk '{ print $NF }' | sed 's/"//g')
    DIR=${DIR/\~/$HOME}
    cd $DIR
}

eend() {
# edit the end of a file with emacs
    FILE=$1
    shift
    emacs +`wc -l "$FILE"` $@
}

function colors() {

    CLR_WHITE="\033[0;37m"
    CLR_WHITEBOLD="\033[1;37m"
    CLR_BLACK="\033[0;30m"
    CLR_GRAY="\033[1;30m"
    CLR_BLUE="\033[1;34m"
    CLR_BLUEBOLD="\033[0;34m"
    CLR_GREEN="\033[0;32m"
    CLR_GREENBOLD="\033[1;32m"
    CLR_CYAN="\033[0;36m"
    CLR_CYANBOLD="\033[1;36m"
    CLR_RED="\033[0;31m"
    CLR_REDBOLD="\033[1;31m"
    CLR_PURPLE="\033[0;35m"
    CLR_PURPLEBOLD="\033[1;35m"
    CLR_YELLOW="\033[0;33m"
    CLR_YELLOWBOLD="\033[1;33m"
    CLR_NOTHING="\033[0m"
}
colors

# nice fast find function
EXCLUDES="(\.svn)|(\.mo$)|(\.po$)|(\.pyc$)"
ff() {

    if (( $# < 2 ))
    then
	FILENAME='*' # default -- look in all files
    else
	FILENAME=$2
    fi
    CMD='command find -L $PWD -iname "${FILENAME}" -print0 2> /dev/null | xargs -r0 grep -il "$1" 2> /dev/null | egrep -v "${EXCLUDES}" 2> /dev/null'
#    echo $CMD
    eval $CMD

}

chainff() {
    if (( $# < 2 ))
    then
	return 0
    fi

    RESULTS=`ff "$2" "$1"`
    shift 2

    for i in $RESULTS
    do
	for arg in $@
	do
	    if grep -il "$arg" "$i" &> /dev/null
	    then
		touch /dev/null
	    else
		i=""		
		break
	    fi
	done
	if [ -n "$i" ]
	then
	    echo $i
	fi
    done
}

# contextual fastfind
cff () {

    if (( $# < 2 )); then
        local FILENAME='*' # default -- look in all files
    else
        local FILENAME=$2
    fi

    for i in `ff "$1" "$FILENAME"`; do
        echo -e "$CLR_GREEN--->>> ""$CLR_YELLOWBOLD""$i""$CLR_NOTHING" :
        grep --color=auto -i -n -C 3 "$1" $i
    done

} 

# make a temporary file
tmpfile() {

if [ "$#" == "0" ]
then
    args="."
else
    args=$@
fi

for i in $args
do
    NEWNAME=${i}.$RANDOM

    while [ -e $NEWNAME ]
    do
	NEWNAME=${NEWNAME}.tmp
    done
    echo "$NEWNAME"
done
}

edpe() {
# edit and pipe the buffer to stdout
FILE=`tmpfile`
$EDITOR $FILE
cat $FILE
rm $FILE
}

swap() {
# swap two files
    if [ "$#" != "2" ]
    then
	echo "Usage: $FUNCNAME <first_arg> <second_arg>"
	return
    fi
    for i in "$1" "$2"
    do
	if [ ! -w "$i" ]
	then
	    echo "$FUNCNAME: Can't move $i"
	    return 1
	fi
    done

    NEWNAME=`basename $1`.$RANDOM

    while [ -e $NEWNAME ]
    do
	NEWNAME=${NEWNAME}.tmp
	echo "$NEWNAME"
    done

    mv `basename $1` $NEWNAME
    mv `basename $2` `basename $1`
    mv $NEWNAME `basename $2`
}

isrunning() {
# is a process running? (by name)
    for i in "$@"
    do
	ps axwww  | grep "$i" | grep -v 'grep'
    done | sort | uniq

}

killbyname() {
# kill a process by name
    kill `isrunning "$@" | awk '{ print $1 }' | onelineit.py`
}


tf() {
    if [[ $@ ]]
    then
	echo "true"
    else
	echo "false"
    fi
}

# full name
fn() {
    python -c "import os; print os.path.realpath('$*')"
}

# which view
whview() {
    less `which $@`
}

# which emacs
whemacs() {
    emacs -nw `which $@`
}

pyfile() {
# python file name
python -c "import $1; print $1.__file__"
}

svndance(){
# do the svn import dance!
if (( $# ))
then
    svn import $1
    cd ..
    rm -rf $OLDPWD
    svn co $1 $OLDPWD
    cd $OLDPWD
else
    return 1
fi
}

difffiles() {
grep '^+++ ' $@ | sed 's/+++ b\///'
}

hg-update-all() { 
for i in *; 
do
    if [ -e $i/.hg ]
    then
        cd $i
        hg pull
        hg update
        cd -
    fi
done
}

### include overrides for commands
source ~/.bash_overrides

### regenerate fluxbox menus here for convenience
MENU=~/web/site/programs.html
if [ -e $MENU ]
then
    html2flux.py $MENU > ~/.fluxbox/applications
fi