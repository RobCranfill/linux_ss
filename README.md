# linux_ss
A screen saver ecosystem for Linux (tested on Ubuntu 25.04) mostly implemented in Python.

The key here is a script (see 'credits' below) that will run a given program as a screen saver.

I then scrounged a bunch of Python/PyGame screen saver apps and incporporated them - with credit, and legitimately I hope.


## Requirements
 * PyGame
 * OpenGL (for 'tnt' module only)
   * something like <code>sudo apt -y install python3-opengl</code>


## Installation

    cp linux_ss.service ~/.config/systemd/user/
    systemctl --user daemon-reload
    systemctl --user enable linux_ss.service
    systemctl --user is-enabled linux_ss.service


## Credits
 * script: https://gist.github.com/vdbsh/a9f0723708a4393d42a0d768d831c4df
 * "kali": https://github.com/steven-halla/screen_saver
 * "mystify": https://github.com/avarokins/Mystify
 * "nboids": https://github.com/Nikorasu/PyNBoids
 * "particles": https://pythonprogramming.altervista.org/particles-screensaver-with-pygame/


## Things to do
 * Make every module use the full screen, and the same 'cancel' key.
 * How to specify path to modules as installed?


###### Copyright (c) 2025  rob cranfill - robcranfill at gmail.com
