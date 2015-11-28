#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import time
import random

start_time = time.time()
slavePuzzle = "mainPuzzle"

RED = [0xfff, 0x0, 0x0]
GREEN = [0x0, 0xfff, 0x0]
BLUE = [0x0, 0x0, 0xfff]
NONE = [0x0, 0x0, 0x0]
def setLedValue(leds, id, color):
    leds[id*3 + 0] = color[0]
    leds[id*3 + 1] = color[1]
    leds[id*3 + 2] = color[2]

def WIRE_CONNECTED(master, task, game_state):
    master.sendGetButtons(slavePuzzle)
    print(master.getButtons(slavePuzzle)[11])
    if master.getButtons(slavePuzzle)[11]:
        return True
    return False

def WIRE_DISCONNECTED(master, task, game_state):
    master.sendGetButtons(slavePuzzle)
    if not master.getButtons(slavePuzzle)[11]:
        return True
    return False

def ENABLE_FUSE_PUZZLE(master, task, game_state):
    leds = master.getSmartLEDs(slavePuzzle)
    setLedValue(leds, 23, GREEN)
    master.sendSetSmartLEDs(slavePuzzle, leds)

def DISABLE_FUSE_PUZZLE(master, task, game_state):
    leds = master.getSmartLEDs(slavePuzzle)
    setLedValue(leds, 23, NONE)
    master.sendSetSmartLEDs(slavePuzzle, leds)

def FUSE_PUZZLE_SOLVED(master, task, game_state):
    master.sendGetButtons(slavePuzzle)
    print(master.getButtons(slavePuzzle))
    if master.getButtons(slavePuzzle)[6] == 1:
        return True
    return False

def FUSE_REMOVED(master, task, game_state):
    master.sendGetStuckButtons(slavePuzzle)
    return False
    return master.getButtons(slavePuzzle)[6] == 0

def ENABLE_RADIO(master, task, game_state):
    print("Radio puzzle solved")
    game_state.add_active_task_with_id(2)

#=============== ADDING TASKS =================================================

def ADD_RANDOM_TASK(master, task, game_state):
    random_id = random.randint(2,3)
    game_state.quest_room.send_ws_message(1, {'message':"Test %s" % random_id})
    game_state.add_active_task_with_id(random_id)

def ADD_FUSE_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(2)

def ADD_DISCONNECT_WIRE(master, task, game_state):
    game_state.add_active_task_with_id(1)

def ADD_CONNECT_WIRE(master, task, game_state):
    game_state.add_active_task_with_id(0)

def ADD_DISABLE_RADIO(master, task, game_state):
    game_state.add_active_task_with_id(3)

def ADD_SEQUENCE_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(4)

def ADD_MECHANICS_CARD_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(5)

def ADD_TUMBLER_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(6)

def ADD_HIDDEN_TUMBLER_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(7)

def ADD_COMMUTATOR_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(8)

def ADD_SECRET(master, task, game_state):
    game_state.add_active_task_with_id(9)

def ADD_ROBOT_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(10)

def ADD_ENGINE_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(11)
#===========================================================
def SECRET_DOORS(master, task, game_state):
    buttonStartPosition = 17
    buttons = master.getButtons(slavePuzzle)[12:18]
    if buttons[3:6] == [0,1,0]:
        relays = buttons[0:3]
        relays.insert(0, 0)
        master.sendSetRelays("capSlave", relays)
    master.sendGetButtons(slavePuzzle)
    return False

def HIDDEN_TUMBLER_PUZZLE_SOLVED(master, task, game_state):
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

def OPEN_FOURTH_BOX(master, task, game_state):
    print("Fourth box was open!")
    leds = master.getSmartLEDs(slavePuzzle)
    ledID = 11
    setLedValue(leds, ledID, BLUE)

    relays = master.getRelays(slavePuzzle)
    relays[3] = 1
    master.sendSetRelays(slavePuzzle, relays)
    master.sendSetSmartLEDs(slavePuzzle, leds)

def OPEN_THIRD_BOX(master, task, game_state):
    print("Third box was open!")
    leds = master.getSmartLEDs(slavePuzzle)
    ledID = 10
    setLedValue(leds, ledID, BLUE)

    relays = master.getRelays(slavePuzzle)
    relays[2] = 1
    master.sendSetRelays(slavePuzzle, relays)
    master.sendSetSmartLEDs(slavePuzzle, leds)

def COMMUTATOR_PUZZLE_SOLVED(master, task, game_state):
    master.sendGetStuckButtons(slavePuzzle)
    if master.getButtons(slavePuzzle)[7] == 1:
        return True
    return False

def TUMBLER_PUZZLE_SOLVED(master, task, game_state):
    leds = master.getSmartLEDs(slavePuzzle)
    ledIdStartPosition = 31
    buttonStartPosition = 17
    buttons = master.getButtons(slavePuzzle)
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

def OPEN_SECOND_BOX(master, task, game_state):
    print("Second box was open!")
    leds = master.getSmartLEDs(slavePuzzle)
    ledID = 9
    setLedValue(leds, ledID, BLUE)

    relays = master.getRelays(slavePuzzle)
    relays[1] = 1
    master.sendSetRelays(slavePuzzle, relays)

    master.sendSetSmartLEDs(slavePuzzle, leds)

def DISABLE_RADIO(master, task, game_state):
    leds = master.getSmartLEDs(slavePuzzle)
    setLedValue(leds, 8, NONE)
    master.sendSetSmartLEDs(slavePuzzle, leds)

lastLockPosition = 0
state = 0

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


def CORRECT_SEQUENCE_ENTERED(master, task, game_state):
    # Сохраняем последнее выбранное значение
    global lastLockPosition, state
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

    #print("LastValue: {}, newValue: {}, state: {} {}".format(
    #    lastLockPosition, lockPosition, state, ACTIVATION_SEQUENCE[state - 1]))

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

def OPEN_FIRST_BOX(master, task, game_state):
    print("First box was open!")
    leds = master.getSmartLEDs(slavePuzzle)
    setLedValue(leds, 8, BLUE) # blue, because blue and green are switched
    relays = master.getRelays(slavePuzzle)
    relays[0] = 1
    master.sendSetRelays(slavePuzzle, relays)
    master.sendSetSmartLEDs(slavePuzzle, leds)

def MECHANICS_CARD_USED(master, task, game_state):
    master.sendGetStuckButtons(slavePuzzle)
    if master.getButtons(slavePuzzle)[10] == 1:
        return True
    return False

def ENABLE_TUMBLER_PUZZLE(master, task, game_state):
    leds = master.getSmartLEDs(slavePuzzle)
    ledIdStartPosition = 31
    for index in range(6):
        ledID = ledIdStartPosition - index
        setLedValue(leds, ledID, RED)
    master.sendSetSmartLEDs(slavePuzzle, leds)

def ROBOT_ASSEMBLED(master, task, game_state):
    leds = master.getSmartLEDs(slavePuzzle)
    ledID = 12
    setLedValue(leds, ledID, RED)
    ledID = 13
    setLedValue(leds, ledID, BLUE)
    ledID = 16
    setLedValue(leds, ledID, [0xfff, 0xfff, 0xfff])

    master.sendSetSmartLEDs(slavePuzzle, leds)

    master.sendGetStuckButtons(slavePuzzle)
    if master.getButtons(slavePuzzle)[8] == 1:
        return True
    return False

def ROBOT_SAY_RIDDLE(master, task, game_state):
    leds = master.getSmartLEDs(slavePuzzle)
    ledID = 12
    setLedValue(leds, ledID, GREEN)
    ledID = 13
    setLedValue(leds, ledID, GREEN)

    master.sendSetSmartLEDs(slavePuzzle, leds)
    print("Robot say RIDDLE!")

def ENGINE_ASSEMBLED(master, task, game_state):
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

def ENABLE_RADIO(master, task, game_state):
    print("Do enable radio")
    leds = master.getSmartLEDs(slavePuzzle)
    setLedValue(leds, 8, [0xfff, 0x0, 0xfff])
    master.sendSetSmartLEDs(slavePuzzle, leds)

def PRESLO_PRESSED(master, task, game_state):
    print(game_state.state['pressed_buttons'])
    print('2' in game_state.state['pressed_buttons'])
    return '2' in game_state.state['pressed_buttons']

KOKOVNIK_PRESSED= lambda master, task, game_state: '3' in game_state.state['pressed_buttons']
TRUNDEL_PRESSED= lambda master, task, game_state: '1' in game_state.state['pressed_buttons']
GLUKALO_PRESSED= lambda master, task, game_state: '0' in game_state.state['pressed_buttons']
