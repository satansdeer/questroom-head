#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import time

slavePuzzle = "mainPuzzle"
slaveCap = "Captain's bridge"


RED = [0xfff, 0x0, 0x0]
GREEN = [0x0, 0xfff, 0x0]
BLUE = [0x0, 0x0, 0xfff]
def setLedValue(leds, id, color):
    leds[id*3 + 0] = color[0]
    leds[id*3 + 1] = color[1]
    leds[id*3 + 2] = color[2]

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
    # master.sendGetButtons(slavePuzzle)
    # time.sleep(.2)
    pass

##############################################


def WIRE_CONNECTED(master, state):
    master.sendGetStuckButtons(slavePuzzle)
    if master.getButtons(slavePuzzle)[11]:
        return True
    return False

def ENABLE_FUSE_PUZZLE(master, state):
    leds = master.getSmartLEDs(slavePuzzle)
    setLedValue(leds, 23, GREEN)
    master.sendSetSmartLEDs(slavePuzzle, leds)

def FUZE_PUZZLE_SOLVED(master, state):
    master.sendGetStuckButtons(slavePuzzle)
    if master.getButtons(slavePuzzle)[6] == 1:
        return True
    return False

def ENABLE_RADIO(master, slave):
    print("Do enable radio")
    leds = master.getSmartLEDs(slavePuzzle)
    setLedValue(leds, 8, [0xfff, 0x0, 0xfff])
    master.sendSetSmartLEDs(slavePuzzle, leds)

lastLockPosition = 0


def turnLeft(lastValue, newValue):
    if lastValue == 255 and newValue == 0:
        return True
    if newValue > lastValue:
        return True
    return False


def turnRigth(lastValue, newValue):
    if lastValue == 0 and newValue == 255:
        return True
    if newValue < lastValue:
        return True
    return False


def turn(lastValue, newValue):
    if turnLeft(lastValue, newValue):
        return "L"
    if turnRigth(lastValue, newValue):
        return "R"


def CORRECT_SEQUENCE_ENTERED(master, state):
    # Сохраняем последнее выбранное значение
    global lastLockPosition
    # Позиция в массиве ADC
    LOCK_ID = 1
    # погрешность
    ERROR_VALUE = 15

    # ACTIVATION_SEQUENCE = ['L', 'L', 'R', 'L', 'R', 'R', 'L', 'R']
    # Последовательность для открытия
    # L - влево; R - вправо
    ACTIVATION_SEQUENCE = ['L', 'L', 'R', 'L']

    if state > len(ACTIVATION_SEQUENCE):
        return True

    master.sendGetADC(slavePuzzle)
    time.sleep(0.4)
    adcArray = master.getADC(slavePuzzle)
    lockPosition = adcArray[LOCK_ID]

    print("LastValue: {}, newValue: {}, state: {} {}".format(
        lastLockPosition, lockPosition, state, ACTIVATION_SEQUENCE[state - 1]))

    if state == 0:
        lastLockPosition = lockPosition
        state = state + 1

    # Смотрим, менялась ли позиция переключателя.
    lessDefault = lastLockPosition < (lockPosition + ERROR_VALUE)
    largeDefault = lastLockPosition > (lockPosition - ERROR_VALUE)
    if lessDefault and largeDefault:
        return state

    if turn(lastLockPosition, lockPosition) == ACTIVATION_SEQUENCE[state -1]:
        state = state + 1
    else:
        state = 0

    lastLockPosition = lockPosition
    return state


def OPEN_FIRST_BOX(master, slave):
    print("First box was open!")
    leds = master.getSmartLEDs(slavePuzzle)
    setLedValue(leds, 8, BLUE)
    relays = master.getRelays(slavePuzzle)
    relays[0] = 1
    master.sendSetRelays(slavePuzzle, relays)
    master.sendSetSmartLEDs(slavePuzzle, leds)

def MECHANICS_CARD_USED(master, state):
    master.sendGetStuckButtons(slavePuzzle)
    if master.getButtons(slavePuzzle)[10] == 1:
        return True
    return False

def ENABLE_TUMBLER_PUZZLE(master, state):
    leds = master.getSmartLEDs(slavePuzzle)
    ledIdStartPosition = 31
    for index in range(6):
        ledID = ledIdStartPosition - index
        setLedValue(leds, ledID, RED)
    master.sendSetSmartLEDs(slavePuzzle, leds)


    # return True

def TUMBLER_PUZZLE_SOLVED(master, state):
    import time
    # start_time = time.time()

    leds = master.getSmartLEDs(slavePuzzle)
    ledIdStartPosition = 31
    buttonStartPosition = 17
    buttons = master.getButtons(slavePuzzle)
    # print("---Time before true {:.3} seconds ---".format(time.time() - start_time))
    master.sendGetButtons(slavePuzzle)

    for index in range(6):
        buttonIndex = buttonStartPosition - index
        ledID = ledIdStartPosition - index
        if buttons[buttonIndex]:
            setLedValue(leds, ledID, BLUE)
        else:
            setLedValue(leds, ledID, RED)
    master.sendSetSmartLEDs(slavePuzzle, leds)

    if buttons[12:18] == [1]*6:
        return True
    return False




def OPEN_SECOND_BOX(master, state):
    print("Second box was open!")
    leds = master.getSmartLEDs(slavePuzzle)
    ledID = 9
    setLedValue(leds, ledID, BLUE)

    relays = master.getRelays(slavePuzzle)
    relays[1] = 1
    master.sendSetRelays(slavePuzzle, relays)

    master.sendSetSmartLEDs(slavePuzzle, leds)


def HIDDEN_TUMBLER_PUZZLE_SOLVED(master, state):
    import time
    start_time = time.time()

    leds = master.getSmartLEDs(slavePuzzle)
    ledIdStartPosition = 0
    buttonStartPosition = 0
    buttons = master.getButtons(slavePuzzle)
    # print("---Time before true {:.3} seconds ---".format(time.time() - start_time))
    master.sendGetButtons(slavePuzzle)
    # timeBeforeFor = time.time()
    for index in range(6):
        buttonIndex = buttonStartPosition + index
        ledID = ledIdStartPosition + index
        if buttons[buttonIndex]:
            setLedValue(leds, ledID, BLUE)
        else:
            setLedValue(leds, ledID, RED)
    master.sendSetSmartLEDs(slavePuzzle, leds)

    if buttons[0:6] == [1]*6:
        return True















    return False

def OPEN_THIRD_BOX(master, state):
    print("Third box was open!")
    leds = master.getSmartLEDs(slavePuzzle)
    ledID = 10
    setLedValue(leds, ledID, BLUE)

    relays = master.getRelays(slavePuzzle)
    relays[2] = 1
    master.sendSetRelays(slavePuzzle, relays)
    master.sendSetSmartLEDs(slavePuzzle, leds)

def COMMUTATOR_PUZZLE_SOLVED(master, state):
    master.sendGetStuckButtons(slavePuzzle)
    if master.getButtons(slavePuzzle)[7] == 1:
        return True
    return False

def OPEN_FOURTH_BOX(master, state):
    print("Fourth box was open!")
    leds = master.getSmartLEDs(slavePuzzle)
    ledID = 11
    setLedValue(leds, ledID, BLUE)

    relays = master.getRelays(slavePuzzle)
    relays[3] = 1
    master.sendSetRelays(slavePuzzle, relays)
    master.sendSetSmartLEDs(slavePuzzle, leds)


def ENGINE_KEY_CORRECT(master, state):
    correctKey = '1258'
    keyInput = input('Enter key:')
    print("You enter: [{}]".format(keyInput), " i wont [{}]". format(correctKey))
    if keyInput == correctKey:
        return True
    return False

def ENGINE_DOOR_OPEN(master, state):
    print("Engine door open")
    relays = master.getRelays(slaveCap)
    relays[2] = 0
    master.sendSetRelays(slaveCap, relays)


def ROBOT_ASSEMBLED(master, state):
    leds = master.getSmartLEDs(slavePuzzle)
    ledID = 12
    setLedValue(leds, ledID, RED)
    ledID = 13
    setLedValue(leds, ledID, BLUE)
    ledID = 16
    setLedValue(leds, ledID, 0xfff, 0xfff, 0xfff)

    master.sendSetSmartLEDs(slavePuzzle, leds)

    master.sendGetStuckButtons(slavePuzzle)
    if master.getButtons(slavePuzzle)[8] == 1:
        return True
    return False

def ROBOT_SAY_RIDDLE(master, state):
    leds = master.getSmartLEDs(slavePuzzle)
    ledID = 12
    setLedValue(leds, ledID, GREEN)
    ledID = 13
    setLedValue(leds, ledID, GREEN)

    master.sendSetSmartLEDs(slavePuzzle, leds)
    print("Robot say RIDDLE!")

def ENGINE_ASSEMBLED(master, state):
    leds = master.getSmartLEDs(slavePuzzle)
    ledID = 20
    setLedValue(leds, ledID, BLUE)
    ledID = 21
    setLedValue(leds, ledID, RED)
    master.sendSetSmartLEDs(slavePuzzle, leds)

    master.sendGetStuckButtons(slavePuzzle)
    if master.getButtons(slavePuzzle)[9] == 1:
        leds = master.getSmartLEDs(slavePuzzle)
        ledID = 20
        setLedValue(leds, ledID, GREEN)
        ledID = 21
        setLedValue(leds, ledID, GREEN)
        master.sendSetSmartLEDs(slavePuzzle, leds)
        return True
    return False

def ACTIVATE_CAPTAIN_BRIDGE(master, state):
    print("Captain bridge activated")
