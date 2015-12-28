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
        self.callbacks = {}
        super(SoundManager, self).__init__()

    def run(self):
        while True:
            for time_key in self.callbacks:
                if time.clock() >= time_key:
                    self.callbacks[time_key]()
                    del self.callbacks[time_key]

    def play_sound(self, sound_name, callback = None):
        sound = pygame.mixer.Sound(sound_name)
        sound.play()
        self.time = time.clock()
        if callback:
            self.callbacks[time.clock() + sound.get_length()] = callback

    def play_keyboard_beep(self):
        self.beep.play()
