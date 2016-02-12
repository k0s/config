#!/bin/bash

### bash rc file ###

# source the profile, if it exists
PROFILE=/etc/profile
if [ -e "${PROFILE}" ]
then
    . "${PROFILE}"
fi

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
export BROWSER=$(which firefox)
export CLICOLOR=1
export EDITOR='emacs -nw'
export JS_EDITLINE=1

# aliases
alias awd="python -c 'import os;  print (os.path.realpath(\".\"))'"
alias currentpatch='echo `hg root`/.hg/patches/`hg qapp -v | tail -n 1 | cut -f 3 -d " "`'
alias datestamp='date +%Y%m%d%H%M%S'
alias envkeys='env | sed "s/=.*//" | sort'
alias grep='grep --colour=auto'
alias loopmplayer='mplayer -fixed-vo -loop 0 -fs'
alias loopxine='xine -f -g -l'
alias lsenv='env | sort | less'
alias mslower='mplayer -osd-fractions 1 -speed 0.1 -osdlevel 3'
alias patch='patch --reject-file=-'
alias random="python -c 'import sys, random; foo = sys.argv[1:]; random.shuffle(foo); print (\" \".join(foo))'"
alias weekstamp="date --date=\"$((`date '+%u'`-1)) days ago\" '+%b %d'"
alias wget='wget --no-check-certificate'
if [ -e ~/.bashttw ]
then
    . ~/.bashttw
fi

# notification: from
# http://www.netinfinity.org/2013/02/4/bits-and-pieces-ubuntu-terminal-notification.html
alias alert_helper='history|tail -n1|sed -e "s/^\s*[0-9]\+\s*//" -e "s/;\s*alert$//"'
alias alert='notify-send -i /usr/share/icons/gnome/32x32/apps/gnome-terminal.png "[$?] $(alert_helper)"'


# PROMPT
PS1='# '
PS2='. '
PROMPT_COMMAND='echo -ne "\033]0;${SSH_CLIENT/*/$HOSTNAME:}${PWD/~/~}\007"'

# PATHs
export PATH=~/firefox:~/bin:~/bin/mozilla:~/python:$PATH:/usr/sbin:/usr/games/bin:~/virtualenv:~/silvermirror/bin:~/smartopen/bin:~/k0s/bin:~/docs/project/ims/workflow:~/cognet/bin:~/cognet/python
export PYTHONPATH=~/python:$PYTHONPATH:~/virtualenv

# clipboard
if which xclip &> /dev/null
then
    export CLIP_COPY="xclip -i"
    export CLIP_PASTE="xclip -o"
elif which pbcopy &> /dev/null
then
    export CLIP_COPY="pbcopy"
    export CLIP_PASTE="pbpaste"
else
    export CLIP_COPY="tee"
    export CLIP_PASTE="true"
fi

### functions

gplot() {

gnuplot -persist <(echo plot '"'$1'"')
}

lspath() {
python -c 'import os; print ("\n".join(os.environ["PATH"].split(os.path.pathsep)))'
}

apply-patch() {
    # apply a patch
    # TODO:
    # - rewrite in python!
    # - extract this general pattern as a bash "decorator" like `lsdiff` in .bash_overrides
    # - right now level=1; make this configurable (somehow)

    if (( ! $# ))
    then
        echo "No patch supplied"
        return 1
    fi

    for patch in $@
    do
        if expr "$1" : 'http[s]\?://.*' &> /dev/null
        then
            IS_URL="true"
        else
            IS__URL="false"
        fi

        if [[ ${IS_URL} == "true" ]]
        then
            if curl --location "${patch}" 2> /dev/null | (command patch -p1 --dry-run &> /dev/null)
            then
                curl --location "${patch}" 2> /dev/null | command patch -p1
                continue
            else
                echo "curl --location ${patch} 2> /dev/null | command patch -p1 --dry-run"
                curl --location "${patch}" 2> /dev/null | command patch -p1 --dry-run
                return $?
            fi
        else
            if patch -p1 --dry-run < ${patch}
            then
                patch -p1 < ${patch}
                continue
            else
                echo "patch -p1 --dry-run < ${patch}"
                patch -p1 --dry-run < ${patch}
                return $?
            fi
        fi
    done
}

cdwin() {
    # change directory to a window's location using its title,
    # as that is set to the cwd by PS1 [?]
    # TODO: ssh windows
    DIR=$(xwininfo | dictify.py xwininfo | awk '{ print $NF }' | sed 's/"//g')
    DIR=${DIR/\~/$HOME}
    cd $DIR
    activate-nearest
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


### find functionality

EXCLUDES="(\.svn)|(\.mo$)|(\.po$)|(\.pyc$)|(\.hg$)|(\.git$)"
ff() {
    # nice fast find function

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
    # chained fast find

    if (( $# < 2 ))
    then
	return 1 # bad invocation
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


cff () {
    # contextual fastfind
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

### functions for files

tmpfile() {
    # make a temporary file if `tempfile` not available

    if [ "$#" == "0" ]
    then
        args="tmp"
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

abspath() {
    # print absolute path
    python -c "import os; print (os.path.realpath('$*'))"
}

fn() {
    # put full name on clipboard and echo it
    python -c "import os; print (os.path.realpath('$*'))" | ${CLIP_COPY}
    ${CLIP_PASTE}
}

swap() {
    # swap two files
    if [ "$#" != "2" ]
    then
	echo "Usage: $FUNCNAME <file1> <file2>"
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

    mv "$1" "$NEWNAME"
    mv "$2" "$1"
    mv "$NEWNAME" "$2"
}

verifyfiles() {
    # verify each line is an existing file
    while read line
    do
        test -e "${line}"
        echo $? $line
    done
}

### functions for editing

edpe() {
    # edit and pipe the buffer to stdout
    FILE=`tmpfile`
    $EDITOR $FILE
    cat $FILE
    rm $FILE
}

eend() {
    # edit the end of a file with emacs
    FILE=$1
    shift
    emacs +`wc -l "$FILE"` $@
}

###

buffer() {
  # temporary buffer with cat and /dev/null
  cat > /dev/null
}

### `which` commands

realwhich() {
    # which -> real paths
    command which $@ | while read line
    do
        python -c "import os; print (os.path.realpath('${line}'))"
    done
}

whview() {
    # which view
    less `realwhich $@`
}

whemacs() {
    # which emacs
    emacs -nw `realwhich $@`
}

lswhich() {
    # ls -l real which
    for i in "$@"
    do
        ls -l $(realwhich $i)
    done
}

### functions for python

pyfile() {
    # python file path
    python -c "import $1; print ($1.__file__)"
}

setup-all() {
    # setup all for development
    # TODO: flowerbed?
    for i in *
    do
        if [ -e "${i}/setup.py" ]
        then
            cd "${i}"
            python setup.py develop
            cd ..
        fi
    done
}

distribute() {
    # upload to pypi
    python setup.py egg_info -RDb "" sdist register upload develop
}

nearest-venv() {
# find the nearest venv
if [[ "$#" == "0" ]]
then
directory=$PWD
else
directory=$1
fi
directory=$(python -c "import os; print (os.path.abspath('${directory}'))")

while [[ "${directory}" != "/" ]]
do
activate="${directory}/bin/activate"
if [ -e "${activate}" ]
then
echo ${directory}
return 0
fi

directory=$(dirname ${directory})

done
return 1
}

activate-nearest() {
# activate the nearest virtualenv
nearest=$(nearest-venv)
activate=${nearest}/bin/activate
if [ -e "${activate}" ]
then
. ${activate}
fi
}

recreate-venv() {
    # recreate a virtualenv
    VIRTUALENV="virtualenv.py"
    if ! which ${VIRTUALENV}
    then
        return 1
    fi
    VENV_PATH=$(which ${VIRTUALENV})
    echo VENV_PATH=${VENV_PATH}

    # update virtualenv if possible
    DIRNAME=$(dirname ${VENV_PATH})
    if [ -d "${DIRNAME}/.git" ]
    then
        cd "${DIRNAME}"
        git pull
        cd --
    fi

    # for each virtualenv given...
    for i in $@
    do
        OLD_PWD=${PWD}
        echo "${i} : OLDPWD=${OLD_PWD}"
        # ...recreate it...
        ${VIRTUALENV} --clear "${i}"

        SRCDIR="${i}"/src
        if [ -d "${SRCDIR}" ]
        then
            . "${i}/bin/activate"
            cd "${SRCDIR}"
            for j in *
            do
                if [ -e "${j}"/setup.py ]
                then
                    cd "${j}"
                    python setup.py develop
                    cd ..
                fi
            done
        fi
        echo "cd OLD_PWD=${OLD_PWD}"
        cd ${OLD_PWD}
    done
}

### functions for version control systems

difffiles() {
    # which files are diffed; could use `lsdiff`
    grep '^+++ ' $@ | sed 's/+++ b\///'
}

git-diff-master() {
    # differences of a git repository with master
    git diff $(git merge-base HEAD master)
}

git-diff-total() {
    # diff of both added + modified files
    combinediff <(git diff) <(git diff --cached)
}

hg-update-all() {
    # update all hg repositories in the current directory
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

hg-qcommit() {
    message=$1
    hg qrefresh
    if [ -z "${message}" ]
    then
        hg qcommit
    else
        hg qcommit -m "${message}"
    fi
    hgroot=$(hg root)
    patches=${hgroot}/.hg/patches/
    if [ -e ${patches}.hg ]
    then
        cd ${patches}
        hg push
    fi
    cd -
}


### functions for web content

blog-file() {
    echo "$HOME/web/blog/k0s/entries/public/$1"
}

###

apt-upgrade() {
sudo apt-get -y update
sudo apt-get -y upgrade
}

flatten() {
  directory=$PWD
  if [ "$#" == "1" ]
  then
      directory=$1
  fi
  cd $directory
  unset find # don't use the alias
  find . -name '*' -type f | sed 's/.\///' | while read line
  do
      filename=$(echo $line | sed 's/\//-/g')
      mv "${line}" "${filename}"
  done
  for i in *
  do
      if [ -d $i ]
      then
          rm -rf "${i}"
      fi
  done
}

filehandles() {
    TMPFILE=$(tmpfile)
    ps -e|grep -v TTY|awk {'print "echo -n \"Process: "$4"\tPID: "$1"\tNumber of FH: \"; lsof -p "$1"|wc -l"'} > ${TMPFILE}
    . ${TMPFILE} | sort
    rm ${TMPFILE}
}

quotemail() {
    # TODO: -> textshaper
command='s/^/> /'
inplace=""
if [ "$#" == "2" ]
then
    inplace="-i"
fi

sed ${inplace} "${command}" "$1"

}

rmktmp() {

TMPDIR=~/tmp
if [ -e ${TMPDIR} ]
then
  rm -rf ${TMPDIR}
fi
mkdir ${TMPDIR}
cd ${TMPDIR}
pwd

}

exists() {
while read line;  do echo ${line} : $(($(test "-e ${line}"\") )); done
}

### ruby version manager
[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*
export PATH="$PATH:$HOME/.rvm/bin" # Add RVM to PATH for scripting

### include overrides for commands
source ~/.bash_overrides

### deactivate any virtualenvs
if type deactivate &> /dev/null
then
deactivate
fi


### source site-specific BASHRC extensions
export CISCO_BASHRC="${HOME}/cisco/bin/.bashrc"
if [ -e "${CISCO_BASHRC}" ]
then
    . "${CISCO_BASHRC}"
fi

### regenerate fluxbox menus here for convenience
MENU=~/web/site/programs.html
regeneratefluxmenu() {
    if [ -e "${MENU}" ]
    then
        html2flux.py "${MENU}" -o ~/.fluxbox/applications
    fi
}
regeneratefluxmenu
