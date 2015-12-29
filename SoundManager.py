from __future__ import print_function
import threading
import time
import pygame
import sys

class SoundManager(threading.Thread):

    def __init__(self):
        pygame.mixer.init()
        beep = pygame.mixer.Sound('sounds/keyboard_1.wav')
        time = 0
        self.callbacks = dict()
        self.callbacks_to_add = dict()
        super(SoundManager, self).__init__()

    def run(self):
        while True:
            timestamp = time.clock()
            callbacks_for_change = self.callbacks.copy()
            for time_key in self.callbacks:
                time_key = float(time_key)
                if timestamp >= time_key:
                    self.callbacks[str(time_key)]()
                    del callbacks_for_change[str(time_key)]
            self.callbacks = callbacks_for_change
            self.callbacks.update(self.callbacks_to_add)
            self.callbacks_to_add = dict()
            
    def play_sound(self, sound_name, callback = None):
        sound = pygame.mixer.Sound(sound_name)
        sound.play()
        self.time = time.clock()
        if callback:
            self.callbacks_to_add[str(time.clock() + sound.get_length())] = callback
            print(self.callbacks)

    def play_keyboard_beep(self):
        self.beep.play()
