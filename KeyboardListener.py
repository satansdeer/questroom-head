from __future__ import print_function
import threading
import pygame
from Getch import getch
# from copy import copy

hallwayPuzzles = "CB_SLAVE_2"
boxes_slave = "CB_SLAVE_1"
class KeyboardListener(threading.Thread):
    PASS_1 = [1,1,1,1]
    TOGGLE_ENTER_DOOR=[7,7,7,7]
    TOGGLE_ENGINE_DOOR=[8,8,8,8]
    TOGGLE_CAPTAIN_DOOR=[9,9,9,9]
    OPEN_ENGINE_DOOR=[1,2,3,4]
    OPEN_CAPTAIN_DOOR=[4,3,2,1]

    TOGGLE_FIRST_BOX=[1,1,1,1]
    TOGGLE_SECOND_BOX=[2,2,2,2]
    TOGGLE_THIRD_BOX=[3,3,3,3]
    TOGGLE_FOURTH_BOX=[4,4,4,4]

    def __init__(self, questMaster):
        pygame.mixer.init(buffer=512)
        self.beep = pygame.mixer.Sound('coin.wav')
        self.beep.set_volume(0.3)
        self.last_keys_pressed = []
        self.questMaster = questMaster
        super(KeyboardListener, self).__init__()
        # self.run()

    def run(self):
        while True:
            char = getch()
            print("Keyboard char: {}".format(char))
            if not char.isdigit():
                continue
            self.beep.play()
            # if self.callback:
            #     self.callback(char)
            self.last_keys_pressed.insert(0, int(char))

            self.toggleDoor(self.TOGGLE_ENTER_DOOR,1)
            self.toggleDoor(self.TOGGLE_ENGINE_DOOR, 2)
            self.toggleDoor(self.TOGGLE_CAPTAIN_DOOR, 3)

            self.toggleBox(self.TOGGLE_FIRST_BOX, 0)
            self.toggleBox(self.TOGGLE_FIRST_BOX, 2)
            self.toggleBox(self.TOGGLE_FIRST_BOX, 3)
            self.toggleBox(self.TOGGLE_FIRST_BOX, 4)

            self.openDoor(self.OPEN_ENGINE_DOOR, 2)
            self.openDoor(self.OPEN_CAPTAIN_DOOR, 3)

    def get_last_keys_pressed():
        retval = self.last_keys_pressed
        self.last_keys_pressed = []
        return retval

    def check(self, password):
        passwordReverse = password[:]
        passwordReverse.reverse()
        if passwordReverse == self.last_keys_pressed[:len(passwordReverse)]:
            self.last_keys_pressed.insert(0, 'a')
            return True
        return False

    def toggleDoor(self, password, doorId):
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
