from __future__ import print_function
import threading
import pygame
from Getch import getch
# from copy import copy

# new version 
import win32api
import win32console
import pythoncom,pyHook

hallwayPuzzles = "CB_SLAVE_2"
boxes_slave = "CB_SLAVE_1"
class KeyboardListener(threading.Thread):
    PASS_1 = [1,1,2,3, 5, 8, 1,3,2,1]
    TOGGLE_ENTER_DOOR=[1,1,2,3, 5, 8, 1,3,2,1]
    TOGGLE_ENGINE_DOOR=[5,7,8,3]
    TOGGLE_CAPTAIN_DOOR=[7,0,6,2]

    TOGGLE_FIRST_BOX=[1,1,1,1,0,0,0,0]
    TOGGLE_SECOND_BOX=[2,2,2,2,0,0,0,0]
    TOGGLE_THIRD_BOX=[3,3,3,3,0,0,0,0]
    TOGGLE_FOURTH_BOX=[4,4,4,4,0,0,0,0]

    def __init__(self, questMaster, game_state):
        pygame.mixer.init(buffer=512)
        self.beep = pygame.mixer.Sound('coin.wav')
        self.beep.set_volume(0.3)
        self.last_keys_pressed = []
        self.questMaster = questMaster
        self.game_state = game_state
        super(KeyboardListener, self).__init__()
        # self.run()

    def OnKeyboardEvent(self, event):
        key = event.Ascii
        if not ord('0') <= key <= ord('9'):
            return True

        keyNumber = int(key - ord('0'))
        print("Keyboard char: {}".format(keyNumber))

        self.beep.play()

        self.last_keys_pressed.insert(0, keyNumber)

        self.toggleDoor(self.TOGGLE_ENTER_DOOR,1)
        self.toggleDoor(self.TOGGLE_ENGINE_DOOR, 2)
        self.toggleDoor(self.TOGGLE_CAPTAIN_DOOR, 3)

        self.toggleBox(self.TOGGLE_FIRST_BOX, 0)
        self.toggleBox(self.TOGGLE_FIRST_BOX, 2)
        self.toggleBox(self.TOGGLE_FIRST_BOX, 3)
        self.toggleBox(self.TOGGLE_FIRST_BOX, 4)
        return True

    def run(self):

        # create a hook manager object
        hm=pyHook.HookManager()
        hm.KeyDown=self.OnKeyboardEvent
        # set the hook
        hm.HookKeyboard()
        # wait forever
        pythoncom.PumpMessages()

    def get_last_keys_pressed():
        retval = self.last_keys_pressed
        self.last_keys_pressed = []
        return retval

    def check(self, password):
        passwordReverse = password[:]
        passwordReverse.reverse()
        if passwordReverse == self.last_keys_pressed[:len(passwordReverse)]:
            self.last_keys_pressed = []
            return True
        return False

    def toggleDoor(self, password, doorId):
        if not self.game_state.canOpenDoor(doorId - 1):
            return

        if self.check(password):
            doors = self.questMaster.getRelays(hallwayPuzzles).get()
            doors[doorId] = 1 if doors[doorId] == 0 else 0
            self.questMaster.setRelays(hallwayPuzzles, doors)

    def toggleBox(self, password, boxId):
        if self.check(password):
            boxes = self.questMaster.getRelays(boxes_slave).get()
            boxes[boxId] = 1 if boxes[boxId] == 0 else 0
            self.questMaster.setRelays(boxes_slave, boxes)

    def openDoor(self, password, doorId):
        if self.check(password):
            doors = self.questMaster.getRelays(hallwayPuzzles).get()
            if doors[doorId] == 1:
                doors[doorId] = 0
                self.questMaster.setRelays(hallwayPuzzles, doors)
