from __future__ import print_function
import threading
from Getch import getch

class KeyboardListener(threading.Thread):
    PASS_1 = [1,1,1,1]
    def __init__(self, master):
        self.master = master
        self.last_keys_pressed = []
        super(KeyboardListener, self).__init__()

    def run(self):
        while True:
            char = getch()
            self.last_keys_pressed.insert(0, char)
            self.checkPassword()

    def get_last_keys_pressed():
        retval = self.last_keys_pressed
        self.last_keys_pressed = []
        return retval


    def checkPassword():
        if self.check(self.PASS_1):
            relays = master.getRelays(captainsBridge).get()
            relays[2] = 1
            master.setRelays(captainsBridge)

        if len(self.last_keys_pressed) > 15:
            self.last_keys_pressed = []




    def check(self, password):
        passwordReverse = copy(password)
        passwordReverse.reverse()
        if passwordReverse == self.last_keys_pressed[:len(passwordReverse)]:
            return True
        return False
