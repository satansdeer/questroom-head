from __future__ import print_function
import threading
import pygame
from Getch import getch

class KeyboardListener(threading.Thread):
    PASS_1 = [1,1,1,1]
    def __init__(self, callback):
        pygame.mixer.init(buffer=512)
        self.beep = pygame.mixer.Sound('coin.wav')
        self.last_keys_pressed = []
        self.callback = callback
        super(KeyboardListener, self).__init__()
        # self.run()

    def run(self):
        while True:
            char = getch()
            print("Keyboard char: {}".format(char))
            self.beep.play()
            if self.callback:
                self.callback(char)
            self.last_keys_pressed.insert(0, char)

    def get_last_keys_pressed():
        retval = self.last_keys_pressed
        self.last_keys_pressed = []
        return retval

    def check(self, password):
        passwordReverse = copy(password)
        passwordReverse.reverse()
        if passwordReverse == self.last_keys_pressed[:len(passwordReverse)]:
            return True
        return False
