#!/bin/bash
# test sending signal to a screensaver

python3 nodes.py &
ss_pid=$!

# echo PID is $ss_pid at `date`

ps aux | grep nodes >lastrun.text

sleep 5

# echo before pkill at `date`

# pkill -SIGTERM $ss_pid
kill -s SIGTERM $ss_pid

# echo after  pkill at `date`

