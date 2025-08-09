"""
Common code to catch a signal.

Just import this module and when the running code gets a SIGTERM,
it will clean up and exit. (Not really any cleanup to do.)
"""

import signal
import sys

def signal_handler(sig, frame):
    """This will handle the signal."""
    # print(f"{__name__} caught signal {sig}!")
    sys.exit(f"{__name__} terminated by SIGTERM")

signal.signal(signal.SIGTERM, signal_handler)
print(f"{__name__} signal handler installed.")
