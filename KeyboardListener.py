from __future__ import print_function
import threading
from Getch import getch

class KeyboardListener(threading.Thread):
    def __init__(self):
        self.last_keys_pressed = []
        super(KeyboardListener, self).__init__()

    def run(self):
        while True:
            char = getch()
            self.last_keys_pressed.insert(0, char)

    def get_last_keys_pressed():
        retval = self.last_keys_pressed
        self.last_keys_pressed = []
        return retval
