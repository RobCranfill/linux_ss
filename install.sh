#!/usr/bin/env bash

# install linux_ss

dest=~/.local/bin/linux_ss/

ss_paths=()
ss_paths+=("kaleid.py")
ss_paths+=("mystify.py")
ss_paths+=("nboids_sp.py")
ss_paths+=("nboids_ss.py")
ss_paths+=("nodes.py")
ss_paths+=("particles.py")
ss_paths+=("tesseract.py")
ss_paths+=("tunnel.py")

for f in "${ss_paths[@]}"
do
  cp -v $f $dest
done
