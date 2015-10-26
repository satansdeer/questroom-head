#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import time

slavePuzzle="mainPuzzle"

# Повторяющиеся функции:
def FIRST_TUMBLER_ON(master, state):
    slavePuzzle = "mainPuzzle"
    # master.sendGetStuckButtons(slavePuzzle)
    print("Requarement: FIRS_TUMBLER_ON: ", master.getButtons(slavePuzzle))
    if master.getButtons(slavePuzzle)[17] == 1:
        print("Button 0 was pressed")
        # raw_input("Press Enter to continue...")
        return True
    return False

# FIRST_TUMBLER_ON = FirstTumblerOn

def TURN_FIRST_LED_GREEN(master, state):
    slavePuzzle = "mainPuzzle"
    leds = master.getSmartLEDs(slavePuzzle)
    print ('"Smart Leds: ', leds)
    leds[31*3 + 0] = 0x00
    leds[31*3 + 1] = 0xfff
    leds[31*3 + 2] = 0x00
    master.sendSetSmartLEDs(slavePuzzle, leds)
    print("Fist led was turn")

def NONE_REQUIREMENT(master, state):
    return True

def GET_STUCK_BUTTONS(master, state):
    master.sendGetButtons(slavePuzzle)
    time.sleep(.2)

##############################################


def WIRE_CONNECTED(master, state):
    master.sendGetStuckButtons(slavePuzzle)
    if master.getButtons(slavePuzzle)[11]:
        return True
    return False

def ENABLE_FUSE_PUZZLE(master, state):
    leds = master.getSmartLEDs(slavePuzzle)
    ledID = 23
    leds[ledID*3 + 0] = 0x00
    leds[ledID*3 + 1] = 0xfff
    leds[ledID*3 + 2] = 0x00
    master.sendSetSmartLEDs(slavePuzzle, leds)

def FUZE_PUZZLE_SOLVED(master, state):
    if master.getButtons(slavePuzzle)[6] == 1:
        return True
    return False

def ENABLE_RADIO(master, slave):
    print("Do enable radio")
    leds = master.getSmartLEDs(slavePuzzle)
    ledID = 8
    leds[ledID*3 + 0] = 0xfff
    leds[ledID*3 + 1] = 0x000
    leds[ledID*3 + 2] = 0x000
    master.sendSetSmartLEDs(slavePuzzle, leds)

def CORRECT_SEQUENCE_ENTERED(master, state):
    lockID = 1
    master.sendGetADC(slavePuzzle)
    adcArray = master.getADC(slavePuzzle)

    if adcArray[lockID] > 240 and adcArray[lockID] <= 255:
        return True
    return False


def OPEN_FIRST_BOX(master, slave):
    print("First box was open!")
    leds = master.getSmartLEDs(slavePuzzle)
    ledID = 8
    leds[ledID*3 + 0] = 0x0
    leds[ledID*3 + 1] = 0x0
    leds[ledID*3 + 2] = 0xfff
    master.sendSetRelays(slavePuzzle, [1, 1, 1, 1])
    master.sendSetSmartLEDs(slavePuzzle, leds)

def MECHANICS_CARD_USED(master, state):
    if master.getButtons(slavePuzzle)[10] == 1:
        return True
    return False

def ENABLE_TUMBLER_PUZZLE(master, state):
    leds = master.getSmartLEDs(slavePuzzle)
    ledIdStartPosition = 31
    for index in range(6):
        ledID = ledIdStartPosition - index
        leds[ledID*3 + 0] = 0xfff
        leds[ledID*3 + 1] = 0x0
        leds[ledID*3 + 2] = 0x0
    # master.sendSetRelays(slavePuzzle, [1, 1, 1, 1])
    master.sendSetSmartLEDs(slavePuzzle, leds)


    # return True

def TUMBLER_PUZZLE_SOLVED(master, state):
    leds = master.getSmartLEDs(slavePuzzle)
    ledIdStartPosition = 31
    buttonStartPosition = 17
    buttons = master.getButtons(slavePuzzle)
    if True:
        master.sendGetStuckButtons(slavePuzzle)
        for index in range(6):
            buttonIndex = buttonStartPosition - index
            ledID = ledIdStartPosition - index
            if buttons[buttonIndex]:
                leds[ledID*3 + 0] = 0x0
                leds[ledID*3 + 1] = 0x0
                leds[ledID*3 + 2] = 0xfff
            else:
                leds[ledID*3 + 0] = 0xfff
                leds[ledID*3 + 1] = 0x0
                leds[ledID*3 + 2] = 0x0
        master.sendSetSmartLEDs(slavePuzzle, leds)
    print("Leds in TumblerPuzzle: \n", leds)
    print("Buttons: ", buttons[12:18])
    if buttons[12:18] == [1]*6:
        return True
    return False




def OPEN_SECOND_BOX(master, state):
    print("Second box was open!")
    leds = master.getSmartLEDs(slavePuzzle)
    ledID = 9
    leds[ledID*3 + 0] = 0x0
    leds[ledID*3 + 1] = 0x0
    leds[ledID*3 + 2] = 0xfff
    master.sendSetRelays(slavePuzzle, [1, 1, 1, 1])
    master.sendSetSmartLEDs(slavePuzzle, leds)


HIDDEN_TUMBLER_PUZZLE_SOLVED = lambda state: True
OPEN_THIRD_BOX = lambda: print("Third box opened")

COMMUTATOR_PUZZLE_SOLVED = lambda state: True
OPEN_FOURTH_BOX = lambda: print("Fourth box opened")

ROBOT_ASSEMBLED = lambda state: True
ROBOT_SAY_RIDDLE = lambda: print("Robot said riddle")

ENGINE_ASSEMBLED = lambda state: True
ACTIVATE_CAPTAIN_BRIDGE = lambda: print("Captain bridge activated")
