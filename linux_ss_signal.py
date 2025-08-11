"""
Common code to catch a signal.

Just import this module and when the running code gets a SIGTERM,
it will clean up and exit. (Not really any cleanup to do.)
"""

import signal
import sys

import pygame


EVENTS_TO_DIE_FOR = (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN)
FPS_FONT = None # we have to wait till after pygame is initted.

def check_for_final_events_and_maybe_die():
    """This will look for the things we look for, and if they happen, we die."""
    for e in pygame.event.get():
        if e.type in EVENTS_TO_DIE_FOR:
            pygame.quit()


def show_fps(screen, clock):
    global FPS_FONT
    if FPS_FONT == None:
        FPS_FONT = pygame.font.Font(None, 30)
    screen.blit(FPS_FONT.render(str(int(clock.get_fps())), True, [0,200,0]), (8, 8))


def signal_handler(sig, frame):
    """This will handle the signal."""
    # print(f"{__name__} caught signal {sig}!")
    sys.exit(f"{__name__} terminated by SIGTERM")

signal.signal(signal.SIGTERM, signal_handler)
print(f"{__name__} signal handler installed.")
