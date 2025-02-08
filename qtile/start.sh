#!/bin/sh

function run {
 if ! pgrep $1 ;
  then
    $@&
  fi
}

#run "lxsession"
#run "udiskie"

run "dunst"
run "picom "
run "nitrogen --restore"

