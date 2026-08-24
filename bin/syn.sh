#!/bin/bash

set -ex

cd

# Same alias as `config` in .bashrc, redefined locally — aliases don't expand
# in non-interactive scripts, only the function form works here.
config() {
  git --git-dir="$HOME/.cfg" --work-tree="$HOME" "$@"
}

~/k0s/bin/silvermirror

config pull
config push
