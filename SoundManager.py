from __future__ import print_function
import threading
import time
import pygame
import sys
from Sound import Sound

def run_in_thread(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
    return run

class SoundManager(threading.Thread):

    def __init__(self):
        beep = Sound('sounds/keyboard_1.wav')
        time = 0
        super(SoundManager, self).__init__()


    def run(self):
        while True:
            pass
            time.sleep(1)


    @run_in_thread
    def play_sound(self, sound_name):
        sound = Sound(sound_name)
        sound.play()


    def play_keyboard_beep(self):
        self.beep.play()
