from __future__ import print_function
import threading
import time
import pygame
import sys

class SoundManager(threading.Thread):

    def __init__(self):
        pygame.mixer.init()
        super(SoundManager, self).__init__()

    def play_sound(self, sound_name):
        sound = pygame.mixer.Sound(sound_name)
        sound.play()
