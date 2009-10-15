#!/bin/bash

desvn() {
    
    if [ "$#" == "1" ]
    then
        cd $1
    fi

    svn ls | grep '.*/$' | while read line
    do
        desvn $line
    done
    rm -rf .svn

    if [ "$#" == "1" ]
    then
        cd ..
    fi


}

desvn