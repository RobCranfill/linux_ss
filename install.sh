#!/usr/bin/env bash

# install linux_ss

dest=~/.local/bin/linux_ss/
mkdir -p $dest

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

cp linux_ss_runner.sh ~/.local/bin

systemctl --user stop       linux_ss.service
cp linux_ss.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable     linux_ss.service
# systemctl --user is-enabled linux_ss.service
systemctl --user start      linux_ss.service
systemctl --user status     linux_ss.service

