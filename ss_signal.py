"""
Common code to catch a signal.
"""

import signal
import sys

def signal_handler(sig, frame):
    print(f"Caught signal {sig}!")
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
print('Press Ctrl+C')
signal.pause()
