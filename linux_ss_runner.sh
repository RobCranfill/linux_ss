#!/usr/bin/env bash

# From https://gist.github.com/vdbsh/a9f0723708a4393d42a0d768d831c4df

# Screensaver functionality for GNOME/Wayland desktops.
# This script will run an arbitrary command after specified time period, 
# if there are no inhibiting applications detected.
# The started process will be terminated at the first user activity.

start_minutes=1 # minutes

# The screensaver modules, and the command to run each.
# (Apparently "~" will be automagically prepended to data file path?!)
ss_paths=()
ss_paths+=('python3 .local/bin/linux_ss/kaleid.py')
ss_paths+=('python3 .local/bin/linux_ss/mystify.py')
ss_paths+=('python3 .local/bin/linux_ss/nboids_sp.py')
ss_paths+=('python3 .local/bin/linux_ss/nboids_ss.py')
ss_paths+=('python3 .local/bin/linux_ss/nodes.py')
ss_paths+=('python3 .local/bin/linux_ss/particles.py')
ss_paths+=('python3 .local/bin/linux_ss/tesseract.py')
ss_paths+=('python3 .local/bin/linux_ss/tunnel.py')

ss_count=${#ss_paths[@]}

lock_screen=false

get_idle_minutes() {
  idle_time=$(dbus-send --print-reply --dest=org.gnome.Mutter.IdleMonitor \
    /org/gnome/Mutter/IdleMonitor/Core org.gnome.Mutter.IdleMonitor.GetIdletime | grep -Po '(?<=uint64\s)\d+')
  if [ -n "$idle_time" ]; then
    echo "$idle_time" / 60000 | bc
  else
    echo "0"
  fi
}

get_inhibitors() {
  for i in $(dbus-send --print-reply --dest=org.gnome.SessionManager \
    /org/gnome/SessionManager org.gnome.SessionManager.GetInhibitors | grep -Po 'Inhibitor\d+'); do
    if dbus-send --print-reply --dest=org.gnome.SessionManager \
      /org/gnome/SessionManager/"$i" org.gnome.SessionManager.Inhibitor.GetFlags | grep -q 'uint32\s8'; then
      true; return
    fi
  done
  false; return
}

while :; do
  if [ "$(get_idle_minutes)" -ge $start_minutes ] && [ -z "$screensaver" ]; then
    if ! get_inhibitors; then

      index=$(($RANDOM % $ss_count))
      cmd=${ss_paths[$index]}

      gnome-session-inhibit $cmd &
      screensaver=$!
    fi
  elif [ "$(get_idle_minutes)" -lt $start_minutes ] && [ -n "$screensaver" ]; then
    if $lock_screen; then
      dbus-send --type=method_call --dest=org.gnome.ScreenSaver \
        /org/gnome/ScreenSaver org.gnome.ScreenSaver.Lock
    fi
    pkill -P $screensaver
    screensaver=""
  fi
  sleep 1
done
