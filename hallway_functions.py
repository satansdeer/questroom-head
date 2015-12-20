#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import time
import random
from Radio import Radio

start_time = time.time()
# slavePuzzle = "mainPuzzle"
hallwayPuzzles = "hallwayPuzzles"
captainsBridge = "captainsBridge"


class LedsIdTable:
    FUSE = 23
    ROBOT_BODY_LEFT = 12
    ROBOT_BODY_RIGHT = 13
    ROBOT_HEAD = 16
    ENGINE_LEFT = 21
    ENGINE_RIGTH = 20
    BOX_1 = 8
    BOX_2 = 9
    BOX_3 = 10
    BOX_4 = 11


class ButtonsIdTable:
    WIRE_CONNECTION = 11
    FUSE = 6
    MECHANICS_CARD = 10
    ROBOT_HEAD = 8
    ENGINE = 9
    COMMUTATOR = 7


class Colors:
    WHITE = [0xff, 0xff, 0xff]
    RED = [0xff, 0x0, 0x0]
    GREEN = [0x0, 0xff, 0x0]
    BLUE = [0x0, 0x0, 0xff]
    NONE = [0x0, 0x0, 0x0]

class AdcIdTable:
    RADIO = 0
    BOX_LOCK = 1


def setLedValue(leds, id, color):
    leds[id * 3 + 0] = color[0]
    leds[id * 3 + 1] = color[1]
    leds[id * 3 + 2] = color[2]


def WIRE_CONNECTED(master, task, game_state):
    wiredConnection = master.getButtons(hallwayPuzzles).get()[
        ButtonsIdTable.WIRE_CONNECTION]
    if wiredConnection:
        return True
    return False


def WIRE_DISCONNECTED(master, task, game_state):
    wiredConnection = master.getButtons(hallwayPuzzles).get()[
        ButtonsIdTable.WIRE_CONNECTION]
    if not wiredConnection:
        return True
    return False


def ENABLE_FUSE_PUZZLE(master, task, game_state):
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.FUSE, Colors.RED)


def DISABLE_FUSE_PUZZLE(master, task, game_state):
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.FUSE, Colors.NONE)


def FUSE_PUZZLE_SOLVED(master, task, game_state):
    buttons = master.getButtons(hallwayPuzzles)
    fuseSolved = buttons.get()[ButtonsIdTable.FUSE]
    if fuseSolved:
        smartLeds = master.getSmartLeds(hallwayPuzzles)
        smartLeds.setOneLed(LedsIdTable.FUSE, Colors.GREEN)
        return True
    return False


def FUSE_REMOVED(master, task, game_state):
    buttons = master.getButtons(hallwayPuzzles)
    fuseSolved = buttons.get()[ButtonsIdTable.FUSE]
    if not (fuseSolved == 1 ):
        return True
    return False

radio = 0

def ENABLE_RADIO(master, task, game_state):
    global radio
    print("Radio puzzle solved")
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.BOX_1, Colors.RED)
    # add radio broadcast
    radio = Radio(0.5, 0.001)

    sounds = [('harp.wav',40.0,80.0), ('island_music_x.wav',120.0,160.0), ('1.wav',200.0,240.0)]

    radio.init_sounds(sounds, 'noize.wav')

    radio.start()

    # radio.set_target_value(15)
    game_state.add_active_task_with_id(12)


def RADIO_BROADCAST(master, task, game_state):
    radioValue = master.getAdc(hallwayPuzzles).get()[AdcIdTable.RADIO]
    #print("Radio value: {}".format(radioValue))
    radio.set_target_value(radioValue)


    

#=============== ADDING TASKS =================================================


class TaskIdTable:
    WIRE_CONNECTED = 0
    WIRE_DISCONNECTED = 1
    FUSE_PUZZLE = 2
    FUSE_REMOVED = 3
    # RADIO_ENABLE =
    # RADIO_DISABLE = 3


def ADD_RANDOM_TASK(master, task, game_state):
    random_id = random.randint(2, 3)
    game_state.quest_room.send_ws_message(
        1, {'message': "Test %s" % random_id})
    game_state.add_active_task_with_id(random_id)


def ADD_CONNECT_WIRE(master, task, game_state):
    game_state.add_active_task_with_id(TaskIdTable.WIRE_CONNECTED)


def ADD_DISCONNECT_WIRE(master, task, game_state):
    game_state.add_active_task_with_id(TaskIdTable.WIRE_DISCONNECTED)


def ADD_FUSE_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(TaskIdTable.FUSE_PUZZLE)

def ADD_FUSE_REMOVED(master, task, game_state):
    game_state.add_active_task_with_id(TaskIdTable.FUSE_REMOVED)

# Включение и Выкл.  радио выполняются в action
# def ADD_DISABLE_RADIO(master, task, game_state):
#     game_state.add_active_task_with_id(3)


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

def ADD_BATTARIES_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(13)

def ADD_ACTIVATE_CAPTAIN_BRIDGE(mastre, task, game_state):
    game_state.add_active_task_with_id(13)
#===========================================================


def SECRET_DOORS(master, task, game_state):
    # buttonStartPosition = 17
    buttons = master.getButtons(hallwayPuzzles).get()[12:18]
    if buttons[3:6] == [0, 1, 0]:
        relays = buttons[0:3]
        relays.insert(0, 0)
        master.setRelays(captainsBridge, relays)
    # master.sendGetButtons(slavePuzzle)
    return False


def HIDDEN_TUMBLER_PUZZLE_SOLVED(master, task, game_state):
    smartLeds = master.getSmartLeds(hallwayPuzzles).get()

    ledIdStartPosition = 0
    buttonStartPosition = 0
    buttons = master.getButtons(hallwayPuzzles).get()
    # print("---Time before true {:.3} seconds ---".format(time.time() - start_time))

    for index in range(6):
        buttonIndex = buttonStartPosition + index
        ledID = ledIdStartPosition + index
        if buttons[buttonIndex]:
            setLedValue(smartLeds, ledID, Colors.BLUE)
        else:
            setLedValue(smartLeds, ledID, Colors.RED)

    master.setSmartLeds(hallwayPuzzles, smartLeds)

    if buttons[0:6] == [1] * 6:
        return True
    return False

def OPEN_FIRST_BOX(master, task, game_state):
    print("First box was open!")
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    # blue, because blue and green are switched
    smartLeds.setOneLed(LedsIdTable.BOX_1, Colors.BLUE)
    relays = master.getRelays(hallwayPuzzles).get()
    relays[0] = 1
    master.setRelays(hallwayPuzzles, relays)

def OPEN_SECOND_BOX(master, task, game_state):
    print("Second box was open!")
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.BOX_2, Colors.BLUE)

    relays = master.getRelays(hallwayPuzzles).get()
    relays[1] = 1
    master.setRelays(hallwayPuzzles, relays)


def OPEN_THIRD_BOX(master, task, game_state):
    print("Third box was open!")
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.BOX_3, Colors.BLUE)

    relays = master.getRelays(hallwayPuzzles).get()
    relays[2] = 1
    master.setRelays(hallwayPuzzles, relays)


def OPEN_FOURTH_BOX(master, task, game_state):
    print("Fourth box was open!")
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.BOX_4, Colors.BLUE)

    relays = master.getRelays(hallwayPuzzles).get()
    relays[3] = 1
    master.setRelays(hallwayPuzzles, relays)




def COMMUTATOR_PUZZLE_SOLVED(master, task, game_state):
    buttons = master.getButtons(hallwayPuzzles).get()
    commutatorSolved = buttons[ButtonsIdTable.COMMUTATOR]
    # if commutatorSolved:
    if True:
        return True
    return False


def TUMBLER_PUZZLE_SOLVED(master, task, game_state):

    smartLeds = master.getSmartLeds(hallwayPuzzles).get()
    ledIdStartPosition = 31
    buttonStartPosition = 17
    buttons = master.getButtons(hallwayPuzzles).get()

    for index in range(6):
        buttonIndex = buttonStartPosition - index
        ledID = ledIdStartPosition - index
        if buttons[buttonIndex]:
            setLedValue(smartLeds, ledID, Colors.BLUE)
        else:
            setLedValue(smartLeds, ledID, Colors.RED)

    master.setSmartLeds(hallwayPuzzles, smartLeds)

    if buttons[12:18] == [1] * 6:
        return True
    return False


def DISABLE_RADIO(master, task, game_state):
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.BOX_1, Colors.NONE)

lastLockPosition = 0
state = 0
# Пока будут глобальными, потом перенесём в стек
# Проблема в следующем. При повороте тумблера возникают шумы, которые
# мы успеваем считывать на нашей скорости. Шумы надо убрать и оставить
# только устоявшиеся значения.
# Чтение с задержкой не подходит - влияет на остальные функции
# Проверим идею.
# На каждом вхождении в функцию будем считывать значение с АЦП
# и складывать в массив. Через определённое количество входений
# выберем то число, которое чаще всех встречается в массиве.
# Проверку можно делать с определённого считывания,
# и продолжать пока какое-нибудь число не повторить больше N раз.

# массив значений
READ_DATA_STACK = []
# максимальная длина массива, после достижение которой массив сброситься
READ_DATA_STACK_LENGTH = 40


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

# def findValue(stack):


def CORRECT_SEQUENCE_ENTERED(master, task, game_state):
    # Сохраняем последнее выбранное значение
    global lastLockPosition, state
    global READ_DATA_STACK, READ_DATA_STACK_LENGTH
    # Позиция в массиве ADC
    LOCK_ID = 1
    # погрешность
    ERROR_VALUE = 15

    # ACTIVATION_SEQUENCE = ['L', 'L', 'R', 'L', 'R', 'R', 'L', 'R']
    # Последовательность для открытия
    # L - влево; R - вправо
    ACTIVATION_SEQUENCE = ['L', 'L', 'R', 'L']
    # time.sleep(0.6)
    if state > len(ACTIVATION_SEQUENCE):
        return True

    value = master.getAdc(hallwayPuzzles).get()[LOCK_ID]
    # READ_DATA_STACK.append(value)


    lockPosition = value

    # print("LastValue: {}, newValue: {}, state: {} {}".format(
    #     lastLockPosition, lockPosition, state, ACTIVATION_SEQUENCE[state - 1]))

    if state == 0:
        lastLockPosition = lockPosition
        state = state + 1

    # Смотрим, менялась ли позиция переключателя.
    lessDefault = lastLockPosition < (lockPosition + ERROR_VALUE)
    largeDefault = lastLockPosition > (lockPosition - ERROR_VALUE)
    if lessDefault and largeDefault:
        return state

    if turn(lastLockPosition, lockPosition) == ACTIVATION_SEQUENCE[state - 1]:
        state = state + 1
    else:
        state = 0

    lastLockPosition = lockPosition


def MECHANICS_CARD_USED(master, task, game_state):
    buttons = master.getButtons(hallwayPuzzles).get()
    cardUsed = buttons[ButtonsIdTable.MECHANICS_CARD]
    if cardUsed:
        return True
    return False


def ENABLE_TUMBLER_PUZZLE(master, task, game_state):
    smartLeds = master.getSmartLeds(hallwayPuzzles).get()
    ledIdStartPosition = 31
    for index in range(6):
        ledID = ledIdStartPosition - index
        setLedValue(smartLeds, ledID, Colors.RED)
    master.setSmartLeds(hallwayPuzzles, smartLeds)


def ROBOT_ASSEMBLED(master, task, game_state):
    buttons = master.getButtons(hallwayPuzzles)
    robbotAssembled = buttons.get()[ButtonsIdTable.ROBOT_HEAD]
    if robbotAssembled:
        smartLeds = master.getSmartLeds(hallwayPuzzles)
        smartLeds.setOneLed(LedsIdTable.ROBOT_BODY_LEFT, Colors.RED)
        smartLeds.setOneLed(LedsIdTable.ROBOT_BODY_RIGHT, Colors.BLUE)
        smartLeds.setOneLed(LedsIdTable.ROBOT_HEAD, Colors.WHITE)
        return True
    return False


def ROBOT_SAY_RIDDLE(master, task, game_state):
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.ROBOT_BODY_LEFT, Colors.GREEN)
    smartLeds.setOneLed(LedsIdTable.ROBOT_BODY_RIGHT, Colors.GREEN)
    smartLeds.setOneLed(LedsIdTable.ROBOT_HEAD, Colors.WHITE)
    print("Robot say RIDDLE!")


def ENGINE_ASSEMBLED(master, task, game_state):
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.ENGINE_RIGTH, Colors.BLUE)
    smartLeds.setOneLed(LedsIdTable.ENGINE_LEFT, Colors.RED)

    buttons = master.getButtons(hallwayPuzzles)
    engineAssembled = buttons.get()[ButtonsIdTable.ENGINE]
    if engineAssembled:
        smartLeds.setOneLed(LedsIdTable.ENGINE_RIGTH, Colors.GREEN)
        smartLeds.setOneLed(LedsIdTable.ENGINE_LEFT, Colors.GREEN)
        return True
    return False


def ACTIVATE_CAPTAIN_BRIDGE(master, state):
    print("Captain bridge activated")


