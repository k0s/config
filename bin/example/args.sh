#!/bin/bash

function foo {
 echo '$*'="$*"
 echo '$@'="$@"
 echo '$#'="$#"
 if [[ "$*" == "test string" ]]
 then
     echo '$*' == "test string"
     if [[ "$@" == "test string" ]]
     then
         echo '$@' == "test string"
     else
         echo '$@' != "test string"
     fi
 fi
}