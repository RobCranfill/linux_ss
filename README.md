# linux_ss
A screen saver ecosystem for Linux (tested on Ubuntu 25.04) mostly implemented in Python.

The key here is a script (see 'credits' below) that will run a given program as a screen saver.

I then scrounged a bunch of Python/PyGame screen saver apps and incporporated them - with credit, and legitimately I hope.


## Requirements
 * PyGame
 * OpenGL (for 'tnt' module only)
   * something like <code>sudo apt -y install python3-opengl</code>


## Installation

    mkdir ~/.local/bin/linux_ss
    cp kaleid.py mystify.py nboids_sp.py nboids_ss.py nodes.py tesseract.py tunnel.py ~/.local/bin/linux_ss

    cp linux_ss.service ~/.config/systemd/user/
    systemctl --user daemon-reload
    systemctl --user enable linux_ss.service
    systemctl --user is-enabled linux_ss.service

ww
## Credits
 * script: https://gist.github.com/vdbsh/a9f0723708a4393d42a0d768d831c4df
 * "kali": https://github.com/steven-halla/screen_saver
 * "mystify": https://github.com/avarokins/Mystify
 * "nboids": https://github.com/Nikorasu/PyNBoids
 * "particles": https://pythonprogramming.altervista.org/particles-screensaver-with-pygame/
 * "tesseract": https://www.reddit.com/r/pygame/comments/15xk7d1/trying_to_make_a_multimonitor_screensaver/


## Things to do
 * Make every module use the full screen.
 * Does Python code need to check cancel key, or will script suffice?
   * If cancel key is needed, all moduels should use the same 'cancel' key.
   * Cancel key may be needed when invoked as stand-alone Python.
 * How to specify path to modules as installed?
 * Rename modules for ease of identification, copying?
   * like "module_xxx.py" ? "linux_ss_module_xxx.py"?


###### Copyright (c) 2025  rob cranfill - robcranfill at gmail.com
