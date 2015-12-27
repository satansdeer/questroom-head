from __future__ import print_function
import threading
import time
import pygame
import sys

class SoundManager(threading.Thread):

    def __init__(self):
        pygame.mixer.init()
        beep = pygame.mixer.Sound('sounds/keyboard_1.wav')
        super(SoundManager, self).__init__()

    def play_sound(self, sound_name):
        sound = pygame.mixer.Sound(sound_name)
        sound.play()

    def play_keyboard_beep(self):
        self.beep.play()
