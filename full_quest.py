#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import time
import random
from Radio import Radio
from collections import Counter
from copy import copy
from threading import Timer
import pygame


class MESSAGE:
    BATTERY_AVALIABLE = "Универсальная батарея Попова №{id} вставлена"
    BATTERY_ABSENT = "ОШИБКА: Универсальная батарея Попова №{id} отсутствует!"
    ENGINE_BROKEN = "Почините двигатель"
    PRESS_HERABORA = "Когда будете готовы - жмите H.E.R.A.B.O.R.A."
    WINNER = "Вы выжили! \nВходная дверь открыта"
    FAIL = "Ваша команда погибла! \nВходная дверь открыта"

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


CB_SLAVE_1="CB_SLAVE_1"
CB_SLAVE_2="CB_SLAVE_2"
hallwayPuzzles = "hallwayPuzzles"

class SOUNDS:
    BOX_OPEN = 'coin.wav'
    ROBOT_SAY_RIDDLE_FIRST_TIME = 'full_robot.wav'
    ROBOT_SAY_RIDDLE_SECOND_TIME = 'robot_second_time.wav'

class ButtonsIdTable:
    WIRE_CONNECTION = 11
    FUSE = 6
    MECHANICS_CARD = 10
    ROBOT_HEAD = 8
    ENGINE = 9
    COMMUTATOR = 7

class CB_CTRL:
    """Named constant for Captain's Bridge controls"""
    # Controller 1
    #    # Buttons
    REPULSIVE_DESYNCRONISER = 0
    LEVITRON = 1
    DEFLECTOR = 2
    BIG_RED_BUTTON = 3
    KRIVOSHUP_MINUS = 4
    KRIVOSHUP_PLUS = 5
    SERVO_COOLING_SYSTEM = 6
    ULTRAFOTON = 13
    REPAIR_NANOROBOTS = 12
    C3PO = 14
    R2D2 = 15
    TETRAGEKS = 16
    #    # ADC
    CLUTCH_REVERSE_CYCLE = 1
    SUPER_BRAIN = 0

    # Controller 2
    #    # Buttons
    TPBACH_1 = 0
    TPBACH_2 = 1
    DVORNIKI = 2
    ECO_LAZER = 3

    BATTERY_1 = 7
    BATTERY_2 = 8
    BATTERY_3 = 10
    BATTERY_4 = 6

    PROTON_LAUNCHERS_BATTERY = 4
    DARK_MATTER_STABILIZER = 5
    HERABORA = 12
    TECHNO = 13
    UGNETATEL = 14
    GIPERBOLOID = 15
    ZOND_JS = 16
    ZOND_JC = 17

    #    # ADC
    CHAMAEMELUM_NOBILE = 0
    DIPSOMANIA_SUPERCHARGER = 1
    HYPER_DRIVE_GENERATOR = 2
    CONDENSER = 7

    DOOR_ENTER = 1
    DOOR_ENGINE = 2
    DOOR_CAPTAIN = 3

class Colors:
    WHITE = [0xfff, 0xfff, 0xfff]
    RED = [0xfff, 0x0, 0x0]
    LIGHT_RED = [0xff, 0x33, 0x33]
    GREEN = [0x0, 0xffF, 0x0]
    LIGHT_GREEN = [0x33, 0xff, 0x33]
    BLUE = [0x0, 0x0, 0xff]
    NONE = [0x0, 0x0, 0x0]

class BASIC_COLORS:
    WHITE = [0xFF, 0xFF, 0xFF]
    RED = [0xff, 0x0, 0x0]
    LIGHT_RED = [0xff, 0x33, 0x33]
    GREEN = [0x0, 0xff, 0x0]
    LIGHT_GREEN = [0x33, 0xff, 0x33]
    BLUE = [0x0, 0x0, 0xff]
    NONE = [0x0, 0x0, 0x0]

    SAND_STORM = [0xff, 0xa8, 0x12]
    # GREEN
    MANTIS = [0x3f, 0xff, 0x00]
    # PURPLE
    PSYCHEDELIC_PURPLE = [0x94, 0x00, 0xd3]
    # PINK
    RASPBERRY_PINK = [0xff, 0x14, 0x93]


def colorTo12Bit(color):
    COLOR_MULT = 16.058
    to16Bit = lambda byte: int(byte * COLOR_MULT)
    return map(to16Bit, color)

class COLORS:
    WHITE = colorTo12Bit(BASIC_COLORS.WHITE)
    RED = colorTo12Bit(BASIC_COLORS.RED)
    LIGHT_RED = colorTo12Bit(BASIC_COLORS.LIGHT_RED)
    GREEN = colorTo12Bit(BASIC_COLORS.GREEN)
    LIGHT_GREEN = colorTo12Bit(BASIC_COLORS.LIGHT_GREEN)
    BLUE = colorTo12Bit(BASIC_COLORS.BLUE)
    NONE = colorTo12Bit(BASIC_COLORS.NONE)
    SAND_STORM = colorTo12Bit(BASIC_COLORS.SAND_STORM)
    PSYCHEDELIC_PURPLE = colorTo12Bit(BASIC_COLORS.PSYCHEDELIC_PURPLE)
    RASPBERRY_PINK = colorTo12Bit(BASIC_COLORS.RASPBERRY_PINK)

class ROOM_LEDS:
    # hallwayPuzzles
    ENTRANCE_TOP = 6
    ENTRANCE_BOTTOM = 14

    ENGINE_ROOM = 7

    # captainsBridge_1
    MAIN_ROOM_TOP = 2
    MAIN_ROOM_BOTTOM = 1
    CAPTAINTS_BRIDGE = 0

def setRoomLight(master, roomLed, color):
    if roomLed in [ROOM_LEDS.ENTRANCE_TOP, ROOM_LEDS.ENTRANCE_BOTTOM, ROOM_LEDS.ENGINE_ROOM]:
        slave = hallwayPuzzles
    elif roomLed in [ROOM_LEDS.MAIN_ROOM_TOP, ROOM_LEDS.MAIN_ROOM_BOTTOM, ROOM_LEDS.CAPTAINTS_BRIDGE]:
        slave = CB_SLAVE_1
    else: return

    leds = master.getSmartLeds(slave)
    leds.setOneLed(roomLed, color)

def RANDOM_ROOM_LIGHT(master):
    LIGHT_RANDOM = [COLORS.WHITE, COLORS.RED, COLORS.LIGHT_RED, COLORS.GREEN, COLORS.LIGHT_GREEN, COLORS.BLUE, COLORS.NONE, COLORS.SAND_STORM, COLORS.PSYCHEDELIC_PURPLE, COLORS.RASPBERRY_PINK]

    lightRandomLen = len(LIGHT_RANDOM)

    randColorId = random.randint(0, lightRandomLen - 1)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, LIGHT_RANDOM[randColorId])

    randColorId = random.randint(0, lightRandomLen - 1)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_BOTTOM, LIGHT_RANDOM[randColorId])

    randColorId = random.randint(0, lightRandomLen - 1)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, LIGHT_RANDOM[randColorId])

    randColorId = random.randint(0, lightRandomLen - 1)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_BOTTOM, LIGHT_RANDOM[randColorId])

    randColorId = random.randint(0, lightRandomLen - 1)
    setRoomLight(master, ROOM_LEDS.ENGINE_ROOM, LIGHT_RANDOM[randColorId])

    randColorId = random.randint(0, lightRandomLen - 1)
    setRoomLight(master, ROOM_LEDS.CAPTAINTS_BRIDGE, LIGHT_RANDOM[randColorId])

class AdcIdTable:
    RADIO = 0
    BOX_LOCK = 1


def setLedValue(leds, id, color):
    leds[id * 3 + 0] = color[0]
    leds[id * 3 + 1] = color[1]
    leds[id * 3 + 2] = color[2]

def REQ_QUEST_INIT(master, task, game_state):


    # close boxes
    #master.setRelays(hallwayPuzzles, [0,0,0,0])
    master.setRelays(hallwayPuzzles, [1,1,1,1])

    # close doors
    # master.setRelays(CB_SLAVE_2, [0,0,0,0])
    master.setRelays(CB_SLAVE_2, [1,1,1,1])


    master.setSmartLeds(hallwayPuzzles, [0,0,0]*32)
    # game_state.quest_room.current_music.play(-1)

    AC_ENABLE_INIT_LIGHTS(master, task, game_state)
    return True

def AC_ENABLE_INIT_LIGHTS(master, task, game_state):
    # Init Lights
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, Colors.NONE)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_BOTTOM, [150, 0, 0])
    setRoomLight(master, ROOM_LEDS.ENGINE_ROOM, Colors.NONE)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, Colors.NONE)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_BOTTOM, Colors.NONE)
    setRoomLight(master, ROOM_LEDS.CAPTAINTS_BRIDGE, Colors.NONE)

def REQ_WIRE_CONNECTED(master, task, game_state):
    wiredConnection = master.getButtons(hallwayPuzzles).get()[
        ButtonsIdTable.WIRE_CONNECTION]
    if wiredConnection:
        return True
    return False

def REQ_WIRE_CONNECTED_AGAIN(master, task, game_state):
    wiredConnection = master.getButtons(hallwayPuzzles).get()[
        ButtonsIdTable.WIRE_CONNECTION]
    if wiredConnection:
        return True
    return False

def REQ_WIRE_DISCONNECTED(master, task, game_state):
    wiredConnection = master.getButtons(hallwayPuzzles).get()[
        ButtonsIdTable.WIRE_CONNECTION]
    if not wiredConnection:
        return True
    return False


def AC_ENABLE_WIRE_ROOMS_COLORS(master, task, game_state):
    RED = 2000
    setRoomLight(master, ROOM_LEDS.ENTRANCE_BOTTOM, [RED, 0, 0])
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_BOTTOM, [RED, 0, 0])


    time.sleep(2)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, [RED, 0, 0])
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, [RED, 0, 0])
    time.sleep(.2)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, Colors.NONE)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, Colors.NONE)

    time.sleep(2)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, [RED, 0, 0])
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, [RED, 0, 0])

    time.sleep(.2)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, Colors.NONE)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, Colors.NONE)
    time.sleep(.1)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, [RED, 0, 0])
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, [RED, 0, 0])
    time.sleep(.2)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, Colors.NONE)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, Colors.NONE)
    time.sleep(.1)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, [RED, 0, 0])
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, [RED, 0, 0])
    time.sleep(.2)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, Colors.NONE)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, Colors.NONE)
    time.sleep(.1)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, [RED, 0, 0])
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, [RED, 0, 0])
    time.sleep(.2)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, Colors.NONE)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, Colors.NONE)
    time.sleep(.1)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, [RED, 0, 0])
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, [RED, 0, 0])
    time.sleep(2)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, [RED, 0, 0])
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, [RED, 0, 0])


def AC_ENABLE_WIRE_ROOMS_LIGHT(master, task, game_state):
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, Colors.RED)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, Colors.RED)
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.FUSE, Colors.RED)

def AC_DISABLE_WIRE_ROOMS_COLORS(master, task, game_state):

    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, Colors.NONE)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_BOTTOM, [150, 0, 0])
    # setRoomLight(master, ROOM_LEDS.ENGINE_ROOM, Colors.NONE)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, Colors.NONE)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_BOTTOM, Colors.NONE)
    # setRoomLight(master, ROOM_LEDS.CAPTAINTS_BRIDGE, Colors.NONE)

def AC_ENABLE_FUSE_ROOMS_COLORS(master, task, game_state):

    wiredConnection = master.getButtons(hallwayPuzzles).get()[
        ButtonsIdTable.WIRE_CONNECTION]
    if not wiredConnection:
        return
    time.sleep(2)
    VIOLENT = [232 * 10, 100 *10, 255 * 10]
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_BOTTOM, [2000, 2000, 2000])
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, VIOLENT)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_BOTTOM, [2000, 2000, 2000])
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, VIOLENT)



def AC_ENABLE_FUSE_ROOMS_LIGHT(master, task, game_state):
    """ only light """
    VIOLENT = [232 * 10, 100 *10, 255 * 10]
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_BOTTOM, [2000, 2000, 2000])
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, VIOLENT)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_BOTTOM, [2000, 2000, 2000])
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, VIOLENT)

    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.FUSE, Colors.GREEN)

def AC_DISABLE_FUSE_ROOMS_COLORS(master, task, game_state):
    wiredConnection = master.getButtons(hallwayPuzzles).get()[
        ButtonsIdTable.WIRE_CONNECTION]
    if not wiredConnection:
        return

    RED = 2000
    time.sleep(1)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_BOTTOM, [RED, 0, 0])
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_BOTTOM, [RED, 0, 0])
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, [RED, 0, 0])
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, [RED, 0, 0])

def AC_ENABLE_ALL_LIGHT(master, task, game_state):
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, COLORS.WHITE)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_BOTTOM, COLORS.WHITE)
    setRoomLight(master, ROOM_LEDS.ENGINE_ROOM, COLORS.WHITE)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, COLORS.WHITE)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_BOTTOM, COLORS.WHITE)
    setRoomLight(master, ROOM_LEDS.CAPTAINTS_BRIDGE, COLORS.WHITE)


def AC_DISABLE_ALL_LIGHT(master, task, game_state):
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, COLORS.NONE)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_BOTTOM, COLORS.NONE)
    setRoomLight(master, ROOM_LEDS.ENGINE_ROOM, COLORS.NONE)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, COLORS.NONE)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_BOTTOM, COLORS.NONE)
    setRoomLight(master, ROOM_LEDS.CAPTAINTS_BRIDGE, COLORS.NONE)

def AC_ENABLE_ROBOT_HEAD_ROOMS_COLORS(master, task, game_state):
    VIOLENT = [232 * 10, 100 *10, 255 * 10]
    time.sleep(2)
    setRoomLight(master, ROOM_LEDS.ENGINE_ROOM, [0, 0, 500])

    setRoomLight(master, ROOM_LEDS.CAPTAINTS_BRIDGE, VIOLENT)


def AC_ENABLE_ENGINE_ROOMS_COLORS(master, task, game_state):
    WHITE = [ 3500, 3500, 3500 ]

    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_BOTTOM, WHITE)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, WHITE)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_BOTTOM, WHITE)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, WHITE)

def AC_ENABLE_FUSE_PUZZLE(master, task, game_state):
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    # smartLeds.setOneLed(LedsIdTable.FUSE, Colors.RED)

    fuseConnection = master.getButtons(hallwayPuzzles).get()[
        ButtonsIdTable.FUSE]

    wiredConnection = master.getButtons(hallwayPuzzles).get()[
        ButtonsIdTable.WIRE_CONNECTION]
    if not wiredConnection:
        return
    if fuseConnection:
        smartLeds.setOneLed(LedsIdTable.FUSE, Colors.GREEN)
    else:
        smartLeds.setOneLed(LedsIdTable.FUSE, Colors.RED)
def AC_DISABLE_FUSE_PUZZLE(master, task, game_state):
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.FUSE, [0x0, 0x0, 0x0])



def REQ_FUSE_PUZZLE_SOLVED(master, task, game_state):
    # return True
    buttons = master.getButtons(hallwayPuzzles)
    fuseSolved = buttons.get()[ButtonsIdTable.FUSE]
    wiredConnection = master.getButtons(hallwayPuzzles).get()[
            ButtonsIdTable.WIRE_CONNECTION]
    if fuseSolved and wiredConnection:
        smartLeds = master.getSmartLeds(hallwayPuzzles)
        smartLeds.setOneLed(LedsIdTable.FUSE, Colors.GREEN)
        return True
    return False


def REQ_FUSE_PUZZLE_SOLVED_AGAIN(master, task, game_state):
    # return True
    buttons = master.getButtons(hallwayPuzzles)
    fuseSolved = buttons.get()[ButtonsIdTable.FUSE]
    if fuseSolved:
        smartLeds = master.getSmartLeds(hallwayPuzzles)
        smartLeds.setOneLed(LedsIdTable.FUSE, Colors.GREEN)
        return True
    return False


def REQ_FUSE_REMOVED(master, task, game_state):
    buttons = master.getButtons(hallwayPuzzles)
    fuseSolved = buttons.get()[ButtonsIdTable.FUSE]
    # print("Fuse state: {}".format(fuseSolved))
    if fuseSolved:
        return False
    # print("FUSE_REMOVED!!!!!!!!!!")
    return True

def AC_ADD_RADIO_BROADCAST(master, task, game_state):
    game_state.add_active_task_with_id(12)


radio = None
radioDisabled = False
def AC_ENABLE_RADIO(master, task, game_state):
    global radioDisabled
    global radio
    print("Radio puzzle solved")
    smartLeds = master.getSmartLeds(hallwayPuzzles)

    relays = master.getRelays(hallwayPuzzles).get()
    if relays[0]:
        smartLeds.setOneLed(LedsIdTable.BOX_1, Colors.RED)
    else:
        smartLeds.setOneLed(LedsIdTable.BOX_1, Colors.BLUE)
    if relays[1]:
        smartLeds.setOneLed(LedsIdTable.BOX_2, Colors.RED)
    else:
        smartLeds.setOneLed(LedsIdTable.BOX_2, Colors.BLUE)
    if relays[2]:
        smartLeds.setOneLed(LedsIdTable.BOX_3, Colors.RED)
    else:
        smartLeds.setOneLed(LedsIdTable.BOX_3, Colors.BLUE)
    if relays[3]:
        smartLeds.setOneLed(LedsIdTable.BOX_4, Colors.RED)
    else:
        smartLeds.setOneLed(LedsIdTable.BOX_4, Colors.BLUE)

    if radio is None:
        # print("========================Radio start!=======================")
        radio = Radio(0.5, 0.001)
        sounds = [('harp.wav',40.0,80.0), ('island_music_x.wav',120.0,160.0), ('leftright_final.wav',200.0,240.0)]
        radio.init_sounds(sounds, 'noize.wav')
        radio.start()

    radioDisabled = False



def REQ_RADIO_BROADCAST(master, task, game_state):
    global radioDisabled
    global radio
    if radioDisabled:
        radio.set_target_value(0)
        return
    radioValue = master.getAdc(hallwayPuzzles).get()[AdcIdTable.RADIO]
    #print("Radio value: {}".format(radioValue))
    if radio:
        radio.set_target_value(radioValue)


def AC_DISABLE_RADIO(master, task, game_state):
    global radioDisabled
    global radio
    # radio.stop()
    radioDisabled = True
    if radio:
        radio.set_target_value(0)


#=============== ADDING TASKS =================================================


class TaskIdTable:
    WIRE_CONNECTED = 100
    WIRE_CONNECTED_AGAIN = 1000
    WIRE_DISCONNECTED = 1
    FUSE_PUZZLE = 2
    FUSE_REMOVED = 3
    FUSE_PUZZLE_AGAIN = 2000
    # RADIO_ENABLE =
    # RADIO_DISABLE = 3


def AC_ADD_CONNECT_WIRE(master, task, game_state):
    game_state.add_active_task_with_id(TaskIdTable.WIRE_CONNECTED)

def AC_ADD_CONNECT_WIRE_AGAIN(master, task, game_state):
    game_state.add_active_task_with_id(TaskIdTable.WIRE_CONNECTED_AGAIN)

def AC_ADD_DISCONNECT_WIRE(master, task, game_state):
    game_state.add_active_task_with_id(TaskIdTable.WIRE_DISCONNECTED)


def AC_ADD_FUSE_PUZZLE(master, task, game_state):
    if not game_state.task_with_id_active(TaskIdTable.FUSE_PUZZLE):
        game_state.add_active_task_with_id(TaskIdTable.FUSE_PUZZLE)

def AC_ADD_FUSE_PUZZLE_AGAIN(master, task, game_state):

    if (not game_state.task_with_id_active(TaskIdTable.FUSE_PUZZLE_AGAIN)) and (not game_state.task_with_id_active(TaskIdTable.FUSE_PUZZLE)):
        game_state.add_active_task_with_id(TaskIdTable.FUSE_PUZZLE_AGAIN)

def AC_ADD_FUSE_REMOVED(master, task, game_state):
    if not game_state.task_with_id_active(TaskIdTable.FUSE_REMOVED):
        game_state.add_active_task_with_id(TaskIdTable.FUSE_REMOVED)

# Включение и Выкл.  радио выполняются в action
# def ADD_DISABLE_RADIO(master, task, game_state):
#     game_state.add_active_task_with_id(3)

def AC_ADD_MECHANICS_CARD_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(5)


def AC_ADD_TUMBLER_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(6)


def AC_ADD_HIDDEN_TUMBLER_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(7)


def AC_ADD_COMMUTATOR_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(8)


def AC_ADD_SECRET(master, task, game_state):
    game_state.add_active_task_with_id(9)


def AC_ADD_ROBOT_PUZZLE(master, task, game_state):
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.ROBOT_BODY_LEFT, Colors.RED)
    smartLeds.setOneLed(LedsIdTable.ROBOT_BODY_RIGHT, Colors.RED)
    smartLeds.setOneLed(LedsIdTable.ROBOT_HEAD, Colors.WHITE)
    game_state.add_active_task_with_id(10)

def AC_ADD_ROBOT_DISASSEMBLED(master, task, game_state):
    game_state.add_active_task_with_id(110)

def AC_ADD_ROBOT_PUZZLE_AGAIN(master, task, game_state):
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.ROBOT_BODY_LEFT, Colors.RED)
    smartLeds.setOneLed(LedsIdTable.ROBOT_BODY_RIGHT, Colors.RED)
    smartLeds.setOneLed(LedsIdTable.ROBOT_HEAD, Colors.WHITE)
    game_state.add_active_task_with_id(111)


def AC_ADD_ENGINE_ROOM_LIGHT(master, task, game_state):
    game_state.add_active_task_with_id(11)

def AC_ADD_BATTARIES_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(13)

def AC_ADD_ACTIVATE_CAPTAIN_BRIDGE(mastre, task, game_state):
    game_state.add_active_task_with_id(13)
#===========================================================


def REQ_SECRET_DOORS(master, task, game_state):
    return True
    buttons = master.getButtons(hallwayPuzzles).get()[12:18]
    if buttons[3:6] == [0, 1, 0]:
        relays = buttons[0:3]
        relays.insert(0, 0)
        master.setRelays(CB_SLAVE_2, relays)
    return False


def AC_OPEN_FIRST_BOX(master, task, game_state):
    print("First box was open!")
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    # blue, because blue and green are switched
    smartLeds.setOneLed(LedsIdTable.BOX_1, Colors.BLUE)
    relays = master.getRelays(hallwayPuzzles).get()
    relays[0] = 0
    master.setRelays(hallwayPuzzles, relays)
    beep = pygame.mixer.Sound(SOUNDS.BOX_OPEN)
    beep.set_volume(0.3)
    beep.play()

def AC_OPEN_SECOND_BOX(master, task, game_state):
    print("Second box was open!")
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.BOX_2, Colors.BLUE)


    relays = master.getRelays(hallwayPuzzles).get()
    relays[1] = 0
    master.setRelays(hallwayPuzzles, relays)

    beep = pygame.mixer.Sound(SOUNDS.BOX_OPEN)
    beep.set_volume(0.3)
    beep.play()

def AC_OPEN_THIRD_BOX(master, task, game_state):
    print("Third box was open!")
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.BOX_3, Colors.BLUE)

    relays = master.getRelays(hallwayPuzzles).get()
    relays[2] = 0
    master.setRelays(hallwayPuzzles, relays)


    beep = pygame.mixer.Sound(SOUNDS.BOX_OPEN)
    beep.set_volume(0.3)
    beep.play()

def AC_OPEN_FOURTH_BOX(master, task, game_state):
    print("Fourth box was open!")
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.BOX_4, Colors.BLUE)

    relays = master.getRelays(hallwayPuzzles).get()
    relays[3] = 0
    master.setRelays(hallwayPuzzles, relays)

    beep = pygame.mixer.Sound(SOUNDS.BOX_OPEN)
    beep.set_volume(0.3)
    beep.play()


def REQ_COMMUTATOR_PUZZLE_SOLVED(master, task, game_state):
    # return True
    buttons = master.getButtons(hallwayPuzzles).get()
    commutatorSolved = buttons[ButtonsIdTable.COMMUTATOR]
    if commutatorSolved:
    #if True:
        return True
    return False


class pColors:
    RED = Colors.RED
    GREEN = Colors.GREEN
    BLUE = Colors.BLUE

def toggleHiddenColor(color):
    if pColors.RED == color:
        color = pColors.BLUE
    else:
        color = pColors.RED
    return color


def toggleVisibleColor(color):
    if pColors.GREEN == color:
        color = pColors.BLUE
    elif pColors.BLUE == color:
        color = pColors.RED
    else:
        color = pColors.GREEN
    return color

# initialization value
hiddenPanelColors = [pColors.RED] * 6
visiblePanelColors = [pColors.RED] * 6

visiblePanelSwitchers = []
oldVisiblePanelSwitchers = [None] * 6
hiddenPanelSwitchers = []
oldHiddenPanelSwitchers = [None] * 6

def REQ_TUMBLER_PUZZLE_SOLVED(master, task, game_state):
    # return True
    global hiddenPanelColors
    global visiblePanelColors

    global visiblePanelSwitchers
    global oldVisiblePanelSwitchers

    global hiddenPanelSwitchers
    global oldHiddenPanelSwitchers

    ELEMENTS_NUMBER = 6
    VISIBLE_SWITCHERS_START_NUM = 12
    VISIBLE_SWITCHERS_END_NUM = 17

    HIDDEN_SWITCHERS_START_NUM = 0
    HIDDEN_SWITCHERS_END_NUM = 5

    buttons = master.getButtons(hallwayPuzzles).get()

    # get values from visible Panel
    visiblePanelSwitchers = buttons[VISIBLE_SWITCHERS_START_NUM:
            VISIBLE_SWITCHERS_END_NUM + 1]
    # doing reverse because num 12 in buttons is 6 on panel
    visiblePanelSwitchers.reverse()

    hiddenPanelSwitchers = buttons[HIDDEN_SWITCHERS_START_NUM:
            HIDDEN_SWITCHERS_END_NUM + 1]

    # print("Visible values: {}".format(visiblePanelSwitchers))
    # print("Hidden values: {}".format(hiddenPanelSwitchers))

    # checked Visible Panel
    for index in range(ELEMENTS_NUMBER):
        if oldVisiblePanelSwitchers[index] != visiblePanelSwitchers[index]:
            # change color for current tumbler
            visiblePanelColors[index] = toggleVisibleColor(
                    visiblePanelColors[index])

            # change color for nex tumbler on the same line
            # on hidden panel
            colorId = index + 1
            # if element before inc was been the last on the line
            # next element been first on the same line
            colorId = colorId % 3
            hiddenPanelColors[colorId] = toggleHiddenColor(
                    hiddenPanelColors[colorId])
    # checked Hidden Panel
    for index in range(ELEMENTS_NUMBER):
        if oldHiddenPanelSwitchers[index] != hiddenPanelSwitchers[index]:
           hiddenPanelColors[index] = toggleHiddenColor(hiddenPanelColors[index])

           colorId = index + 1
           colorId = colorId % 3
           visiblePanelColors[colorId] = toggleVisibleColor(
                   visiblePanelColors[colorId])

    # save new values in global lists
    oldVisiblePanelSwitchers = visiblePanelSwitchers[:]
    oldHiddenPanelSwitchers = hiddenPanelSwitchers[:]

    # set new colors on device
    # 12 times executed function, whom used Rlock
    # It's might be critical
    smartLedsObj = master.getSmartLeds(hallwayPuzzles)
    for index in range(ELEMENTS_NUMBER):
        smartLedsObj.setOneLed(index, hiddenPanelColors[index])
        # NUM_LEDS 32, but index from 0 to 31
        visibleIndex = smartLedsObj.NUM_LEDS - 1 - index
        smartLedsObj.setOneLed(visibleIndex, visiblePanelColors[index])

    WINNER_COLOR_LIST= [pColors.BLUE] * 6
    visiblePanelState = (WINNER_COLOR_LIST == visiblePanelColors)
    hiddenPanelState = (WINNER_COLOR_LIST == hiddenPanelColors)

    return visiblePanelState and hiddenPanelState


lastLockPosition = None
state = 0
# массив значений
READ_DATA_STACK = []
# максимальная длина массива, после достижение которой массив сброситься
READ_DATA_STACK_LENGTH = 200

def turnLeft(lastValue, newValue):
    if lastValue == 255 and newValue == 0:
        return True
    elif lastValue == 0 and newValue == 255:
        return False
    elif newValue > lastValue:
        return True
    return False


def turnRigth(lastValue, newValue):
    if lastValue == 0 and newValue == 255:
        return True
    elif lastValue == 255 and newValue == 0:
        return False
    elif newValue < lastValue:
        return True
    return False


def turn(lastValue, newValue):
    if turnLeft(lastValue, newValue):
        return "L"
    if turnRigth(lastValue, newValue):
        return "R"

lockRead = True
def readLockTimeout():
    global lockRead
    # print("ReadLockTimeout")
    # if lockRead:
    #     lockRead = False
    # else:
    #     lockRead = True
    lockRead = True

CORRECT_LED = False
correctLedTimerDescriptor = None
def enableCorrectLedTimeout(master):
    global CORRECT_LED
    global OPEN_FLAG
    global correctLedTimerDescriptor
    correctLedTimerDescriptor = None
    print("CORRECT_LED_DISABLE")
    CORRECT_LED = False
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    if OPEN_FLAG:
        # smartLeds.setOneLed(LedsIdTable.BOX_1, Colors.BLUE)
        pass
    else:
        smartLeds.setOneLed(LedsIdTable.BOX_1, Colors.RED)

sequencePeriodicRead = None
def AC_ADD_SEQUENCE_PUZZLE(master, task, game_state):
    global sequencePeriodicRead
    global READ_SEQUENCE_DELAY
    sequencePeriodicRead = Timer(READ_SEQUENCE_DELAY, readLockTimeout)
    sequencePeriodicRead.start()
    if not game_state.task_with_id_active(4):
        game_state.add_active_task_with_id(4)

# def findValue(stack):
OPEN_FLAG = False
PLAYER_SEQUENCE=[]
READ_SEQUENCE_DELAY = 0.05
CORRECT_LED_TIMEOUT = 0.05
def REQ_CORRECT_SEQUENCE_ENTERED(master, task, game_state):
    # return True
    # Сохраняем последнее выбранное значение
    global lastLockPosition, state
    global PLAYER_SEQUENCE
    global READ_DATA_STACK, READ_DATA_STACK_LENGTH
    global lockRead
    global sequencePeriodicRead
    global READ_SEQUENCE_DELAY
    global OPEN_FLAG
    global CORRECT_LED, CORRECT_LED_TIMEOUT, correctLedTimerDescriptor
    # Позиция в массиве ADC
    LOCK_ID = 1
    # погрешность
    ERROR_VALUE = 15

    # ACTIVATION_SEQUENCE = ['L', 'L', 'R', 'L', 'R', 'R', 'L', 'R']
    # Последовательность для открытия
    # L - влево; R - вправо
    ACTIVATION_SEQUENCE = ['L', 'L', 'R', 'L']
    # time.sleep(0.6)
    if lockRead:
        value = master.getAdc(hallwayPuzzles).get()[LOCK_ID]
        READ_DATA_STACK.append(value)

    if len(READ_DATA_STACK) < READ_DATA_STACK_LENGTH:
    # if len(READ_DATA_STACK) != READ_DATA_STACK_LENGTH:
        return

    lockRead = False
    sequencePeriodicRead = Timer(READ_SEQUENCE_DELAY, readLockTimeout)
    sequencePeriodicRead.start()

    result = READ_DATA_STACK[0]
    for val in READ_DATA_STACK[1:]:
        if abs(val - result) > 5:
            READ_DATA_STACK = []
            return
        result = val


    PLAYER_SEQUENCE = PLAYER_SEQUENCE[:len(ACTIVATION_SEQUENCE)]
    # get most freq value
    value = Counter(READ_DATA_STACK).most_common(1)[0][0]
    savedStack = READ_DATA_STACK[:]
    READ_DATA_STACK = []


    lockPosition = value
    if lastLockPosition is None:
        lastLockPosition = lockPosition

    # Смотрим, менялась ли позиция переключателя.
    lessDefault = lastLockPosition < (lockPosition + ERROR_VALUE)
    largeDefault = lastLockPosition > (lockPosition - ERROR_VALUE)
    if lessDefault and largeDefault:
        lastLockPosition = lockPosition
        return False
    print("="*80 + "\n==")
    print("lastLockPosition: {}, lockPosition: {}".format(lastLockPosition, lockPosition))
    turnDirection = turn(lastLockPosition, lockPosition)
    print("We turn to the: {}".format(turnDirection))
    print("==\n ={}\n".format(savedStack))
    PLAYER_SEQUENCE.insert(0, turnDirection)
    if not CORRECT_LED:
        if correctLedTimerDescriptor is None:
            correctLedTimerDescriptor = Timer(CORRECT_LED_TIMEOUT, enableCorrectLedTimeout, [master])
            correctLedTimerDescriptor.start()
            CORRECT_LED = True
            smartLeds = master.getSmartLeds(hallwayPuzzles)
            smartLeds.setOneLed(LedsIdTable.BOX_1, Colors.GREEN)

    reversePlayerSequence = copy(PLAYER_SEQUENCE[:len(ACTIVATION_SEQUENCE)])
    reversePlayerSequence.reverse()
    print("Player sequence: {} \n reverse: {}".format(PLAYER_SEQUENCE, reversePlayerSequence))

    if ACTIVATION_SEQUENCE == reversePlayerSequence:
        print("We opened lock box: sleep!!!")
        PLAYER_SEQUENCE = []
        smartLeds = master.getSmartLeds(hallwayPuzzles)
        if OPEN_FLAG:
        # blue, because blue and green are switched
            OPEN_FLAG = False
            # smartLeds.setOneLed(LedsIdTable.BOX_1, Colors.BLUE)
        else:
            OPEN_FLAG = True
            # smartLeds.setOneLed(LedsIdTable.BOX_1, Colors.RED)
        # return  False
        return  True

    lastLockPosition = lockPosition


def REQ_MECHANICS_CARD_USED(master, task, game_state):
    # return True
    buttons = master.getButtons(hallwayPuzzles).get()
    cardUsed = buttons[ButtonsIdTable.MECHANICS_CARD]
    if cardUsed:
        return True
    return False


def AC_ENABLE_TUMBLER_PUZZLE(master, task, game_state):
    smartLeds = master.getSmartLeds(hallwayPuzzles).get()
    ledIdStartPosition = 31
    for index in range(6):
        ledID = ledIdStartPosition - index
        setLedValue(smartLeds, ledID, Colors.RED)
        setLedValue(smartLeds, index, Colors.RED)
    master.setSmartLeds(hallwayPuzzles, smartLeds)

def AC_ENABLE_TUMBLER_PUZZLE_LIGHT_WIN(master, task, game_state):
    smartLeds = master.getSmartLeds(hallwayPuzzles).get()
    ledIdStartPosition = 31
    for index in range(6):
        ledID = ledIdStartPosition - index
        setLedValue(smartLeds, ledID, Colors.BLUE)
        setLedValue(smartLeds, index, Colors.BLUE)
    master.setSmartLeds(hallwayPuzzles, smartLeds)

def REQ_ROBOT_ASSEMBLED(master, task, game_state):
    # return True
    buttons = master.getButtons(hallwayPuzzles)
    robotAssembled = buttons.get()[ButtonsIdTable.ROBOT_HEAD]
    if robotAssembled:

        smartLeds = master.getSmartLeds(hallwayPuzzles)

        smartLeds.setOneLed(LedsIdTable.ROBOT_BODY_LEFT, Colors.GREEN)
        smartLeds.setOneLed(LedsIdTable.ROBOT_BODY_RIGHT, Colors.RED)
        smartLeds.setOneLed(LedsIdTable.ROBOT_HEAD, Colors.WHITE)
        return True
    return False

def REQ_ROBOT_DISASSEMBLED(master, task, game_state):
    buttons = master.getButtons(hallwayPuzzles)
    robotAssembled = buttons.get()[ButtonsIdTable.ROBOT_HEAD]
    return not robotAssembled

robotWasAssembled = False
def AC_ROBOT_SAY_RIDDLE(master, task, game_state):
    smartLeds = master.getSmartLeds(hallwayPuzzles)

    smartLeds.setOneLed(LedsIdTable.ROBOT_BODY_LEFT, [0, 0xfff, 750])
    smartLeds.setOneLed(LedsIdTable.ROBOT_BODY_RIGHT, [0xfff, 0x0, 0x0])

    smartLeds.setOneLed(LedsIdTable.ROBOT_HEAD, [0xff, 0xff, 0xff])

    # play robot
    global robotWasAssembled
    if not robotWasAssembled:
        robotWasAssembled = True
        game_state.quest_room.play_robot(SOUNDS.ROBOT_SAY_RIDDLE_FIRST_TIME)
    else:
        game_state.quest_room.play_robot(SOUNDS.ROBOT_SAY_RIDDLE_SECOND_TIME)

    print("Robot say RIDDLE!")




def AC_ACTIVATE_CAPTAIN_BRIDGE(master, state):
    print("Captain bridge activated")



def REQ_TRUE(master, task, game_state):
    return True

def AC_ADD_CHECK_ENGINE_AND_BATTERIES(master, task, game_state):
    game_state.send_time_to_monitors = False
    game_state.add_active_task_with_id(101)


def AC_INIT(master, task, game_state):
    taskList = [151, 152, 153, 154, 102, 101]
    for taskId in taskList:
        game_state.add_active_task_with_id(taskId)

def AC_ALLOW_DOOR_OPEN(master, task, game_state):
    # allow open Engine door from keyboard
    game_state.allowOpenDoor(1)
    # allow open Captain door from keyboard
    game_state.allowOpenDoor(2)

def REQ_ENGINE_ASSEMBLED(master, task, game_state):
    # return True
    buttons = master.getButtons(hallwayPuzzles)
    engineAssembled = buttons.get()[ButtonsIdTable.ENGINE]
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    # print("We in req_engine")

    if engineAssembled:
        return True
    return False

batterys_saved_state = []
engine_saved_state = None
def REQ_CHECK_BATTERIES(master, task, game_state):

    global batterys_saved_state, engine_saved_state

    buttons = master.getButtons(CB_SLAVE_2).get()
    batterys_state = [1] * 5
    batterys_state[1] = buttons[CB_CTRL.BATTERY_1]
    batterys_state[2] = buttons[CB_CTRL.BATTERY_2]
    batterys_state[3] = buttons[CB_CTRL.BATTERY_3]
    batterys_state[4] = buttons[CB_CTRL.BATTERY_4]

    batterys_state_changed = batterys_state != batterys_saved_state
    if batterys_state_changed:
        batterys_saved_state = copy(batterys_state)

    buttons = master.getButtons(hallwayPuzzles)
    engineAssembled = buttons.get()[ButtonsIdTable.ENGINE]
    smartLeds = master.getSmartLeds(hallwayPuzzles)

    engine_state_changed = engine_saved_state != engineAssembled
    if engine_state_changed:
        engine_saved_state = engineAssembled

    if engineAssembled:

        if engine_state_changed:
            smartLeds.setOneLed(LedsIdTable.ENGINE_RIGTH, Colors.GREEN)
            smartLeds.setOneLed(LedsIdTable.ENGINE_LEFT, Colors.GREEN)

        if batterys_state_changed or engine_state_changed:
            for index in range(1,5):
                monitorId = index
                batteryId = index
                sendBatteryMessage(game_state, monitorId, batterys_state[index], batteryId)
    else:

        if engine_state_changed:
            smartLeds.setOneLed(LedsIdTable.ENGINE_RIGTH, Colors.BLUE)
            smartLeds.setOneLed(LedsIdTable.ENGINE_LEFT, Colors.RED)
            for monitorId in range(1,5):
                sendMessageToMonitor(game_state, monitorId, MESSAGE.ENGINE_BROKEN, False)

    batteryState = all( state is 1 for state in batterys_state) and engineAssembled

    return batteryState


def sendBatteryMessage(game_state, monitorId, battery, batteryId):
    if battery:
        sendMessageToMonitor(game_state, monitorId, MESSAGE.BATTERY_AVALIABLE.format(id=batteryId), False, True)
    else:
        sendMessageToMonitor(game_state, monitorId, MESSAGE.BATTERY_ABSENT.format(id=batteryId), False)

def sendMessageToMonitor(game_state, monitorId, message, progress_bar_visible, not_a_task=False):
    game_state.quest_room.send_ws_message(str(monitorId), {'message': message, 'progress_visible': progress_bar_visible, 'not_a_task': not_a_task})



def AC_PRESS_HERABORA(master, task, game_state):
    for monitorId in range(1,5):
        sendMessageToMonitor(game_state, monitorId, MESSAGE.PRESS_HERABORA, False)
        # game_state.quest_room.send_ws_message(str(monitorId), {'message': MESSAGE.PRESS_HERABORA})
    # added REQ_CHECK_HERABORA task and instructions
    game_state.add_active_task_with_id(201)

def AC_SHOW_GAME_INSTRUCTIONS(master, task, game_state):

    cb_controller = game_state.cb_controller

    cb_controller.initialization()
    cb_controller.show_initialization_messages()
    # added REQ_CHECK_HERABORA and start game
    game_state.add_active_task_with_id(202)

def AC_FINAL_GAME_MUSIC_START(master, task, game_state):
    game_state.quest_room.current_music.stop()
    game_state.quest_room.current_music = game_state.quest_room.final_game_music
    game_state.quest_room.current_music.play(-1)

def AC_WIN_MUSIC_START(master, task, game_state):
    game_state.quest_room.current_music.stop()
    game_state.quest_room.current_music = game_state.quest_room.win_music
    game_state.quest_room.current_music.play(-1)

def REQ_CHECK_HERABORA(master, task, game_state):
        heraboraPressed = master.getButtons(CB_SLAVE_2).get()[12]
        #print("Herabora value: {}\n", heraboraPressed)
        return heraboraPressed

def AC_CB_ADD_RANDOM_TASK(master, task, game_state):
    pass
    # monitorId = game_state.getMonitorIdByTask(task)

    # print("RANDOM TASK: {} done:monitorID {}".format(task.id, monitorId))
    # game_state.quest_room.send_ws_message(str(monitorId), {'message': "OK"})
    # game_state.add_cb_random_task()

def AC_ADD_END_GAME_TASK(master, task, game_state):
    game_state.send_time_to_monitors = False
    game_state.add_active_task_with_id(203)

def REQ_CAPTAINS_BRIDGE_GAME_SUCCESS(master, task, game_state):

    cb_controller = game_state.cb_controller
    return cb_controller.check()

def AC_ENTERED_DOOR_OPEN(master, task, game_state):
    relays = master.getRelays(CB_SLAVE_2).get()
    relays[CB_CTRL.DOOR_ENTER] = 0
    master.setRelays(CB_SLAVE_2, relays)

    print("Entered door opened")

def AC_SHOW_SUCCESS_MESSAGE(master, task, game_state):
    print("You are WINNER!")

    for monitorId in range(1,5):
        sendMessageToMonitor(game_state, monitorId, MESSAGE.WINNER, False)

def AC_RANDOM_ROOM_LIGHT(master, task, game_state):
    start_time = time.time()
    cur_time = time.time()
    ACTION_TIME = 60 * 1

    while (cur_time - start_time) < ACTION_TIME:
        RANDOM_ROOM_LIGHT(master)
        time.sleep(0.1)
        cur_time = time.time()


    setRoomLight(master, ROOM_LEDS.ENTRANCE_TOP, COLORS.WHITE)
    setRoomLight(master, ROOM_LEDS.ENTRANCE_BOTTOM, COLORS.WHITE)
    setRoomLight(master, ROOM_LEDS.ENGINE_ROOM, COLORS.WHITE)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_TOP, COLORS.WHITE)
    setRoomLight(master, ROOM_LEDS.MAIN_ROOM_BOTTOM, COLORS.WHITE)
    setRoomLight(master, ROOM_LEDS.CAPTAINTS_BRIDGE, COLORS.WHITE)

def REQ_AMOUNT_OF_TASK_FAILURE(master, task, game_state):
    if 0 == game_state.cb_controller.current_lives_num:
            return True
    return False

def AC_SHOW_FAILURE_MESSAGE(master, task, game_state):
    game_state.cb_controller.remove_random_tasks()

    for monitorId in range(1,5):
        sendMessageToMonitor(game_state, monitorId, MESSAGE.FAIL, False)

    print("+"*80+"You lose" + "+" * 80)

# Tasks

def REQ_CB_TASK_FAILURE(master, task, game_state):
    """ Failure requarement for Captain's bridge tasks """
    return game_state.cbTaskFailure(task)




def REQ_SERVO_COOLING_SYSTEM_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return buttons[CB_CTRL.SERVO_COOLING_SYSTEM]

def REQ_SERVO_COOLING_SYSTEM_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.SERVO_COOLING_SYSTEM]

def REQ_DEFLECTOR_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.DEFLECTOR]

def REQ_DEFLECTOR_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.DEFLECTOR]

def REQ_LEVITRON_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.LEVITRON]

def REQ_LEVITRON_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.LEVITRON]

def REQ_KRIVOSHUP_PLUS_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.KRIVOSHUP_PLUS]

def REQ_KRIVOSHUP_PLUS_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.KRIVOSHUP_PLUS]

def REQ_KRIVOSHUP_MINUS_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.KRIVOSHUP_MINUS]

def REQ_KRIVOSHUP_MINUS_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.KRIVOSHUP_MINUS]

def REQ_REPULSIVE_DESYCHRONISER_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.REPULSIVE_DESYNCRONISER]

def REQ_REPULSIVE_DESYCHRONISER_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.REPULSIVE_DESYNCRONISER]

def REQ_BIG_RED_BUTTON_PRESSED(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.BIG_RED_BUTTON]

def REQ_CLUTCH_REVERSE_SYCLE_TO_0(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 0 == adc[CB_CTRL.CLUTCH_REVERSE_CYCLE]

def REQ_CLUTCH_REVERSE_SYCLE_TO_77(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 77 == adc[CB_CTRL.CLUTCH_REVERSE_CYCLE]

def REQ_CLUTCH_REVERSE_SYCLE_TO_150(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 150 == adc[CB_CTRL.CLUTCH_REVERSE_CYCLE]

def REQ_CLUTCH_REVERSE_SYCLE_TO_255(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 255 == adc[CB_CTRL.CLUTCH_REVERSE_CYCLE]

def REQ_SUPER_BRAIN_TO_0(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 0 == adc[CB_CTRL.SUPER_BRAIN]

def REQ_SUPER_BRAIN_TO_255(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 255 == adc[CB_CTRL.SUPER_BRAIN]

def REQ_SUPER_BRAIN_TO_182(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 182 == adc[CB_CTRL.SUPER_BRAIN]

def REQ_SUPER_BRAIN_TO_129(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 129 == adc[CB_CTRL.SUPER_BRAIN]

def REQ_SUPER_BRAIN_TO_86(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 86 == adc[CB_CTRL.SUPER_BRAIN]

def REQ_SUPER_BRAIN_TO_45(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 45 == adc[CB_CTRL.SUPER_BRAIN]

# Panel 1_2

def REQ_TETRAGEKS_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.TETRAGEKS]

def REQ_TETRAGEKS_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.TETRAGEKS]

def REQ_C3PO_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.C3PO]

def REQ_C3PO_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.C3PO]

def REQ_R2D2_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.R2D2]

def REQ_R2D2_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.R2D2]

def REQ_REPAIR_NANOROBOTS_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.REPAIR_NANOROBOTS]

def REQ_REPAIR_NANOROBOTS_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.REPAIR_NANOROBOTS]

def REQ_ULTRAFOTON_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.ULTRAFOTON]

def REQ_ULTRAFOTON_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.ULTRAFOTON]

# Panel 2_3

def REQ_TPBACH_1_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.TPBACH_1]

def REQ_TPBACH_1_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 0 == buttons[CB_CTRL.TPBACH_1]

def REQ_TPBACH_2_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.TPBACH_2]

def REQ_TPBACH_2_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 0 == buttons[CB_CTRL.TPBACH_2]

def REQ_ECO_LAZER_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.ECO_LAZER]

def REQ_ECO_LAZER_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 0 == buttons[CB_CTRL.ECO_LAZER]

def REQ_DARK_MATTER_STABILIZER_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.DARK_MATTER_STABILIZER]

def REQ_DARK_MATTER_STABILIZER_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 0 == buttons[CB_CTRL.DARK_MATTER_STABILIZER]

def REQ_DVORNIKI_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.DVORNIKI]

def REQ_DVORNIKI_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 0 == buttons[CB_CTRL.DVORNIKI]

def REQ_PROTON_LAUNCHERS_BATTERY_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.PROTON_LAUNCHERS_BATTERY]

def REQ_PROTON_LAUNCHERS_BATTERY_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 0 == buttons[CB_CTRL.PROTON_LAUNCHERS_BATTERY]

def REQ_HYPER_DRIVE_GENERATOR_TO_MAX(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 255 == adc[CB_CTRL.HYPER_DRIVE_GENERATOR]

def REQ_HYPER_DRIVE_GENERATOR_TO_MIN(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 0 == adc[CB_CTRL.HYPER_DRIVE_GENERATOR]

def REQ_DIPSOMANIA_SUPERCHARGER_TO_3(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 130 == adc[CB_CTRL.DIPSOMANIA_SUPERCHARGER]

def REQ_DIPSOMANIA_SUPERCHARGER_TO_2(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 86 == adc[CB_CTRL.DIPSOMANIA_SUPERCHARGER]

def REQ_DIPSOMANIA_SUPERCHARGER_TO_1(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 45 == adc[CB_CTRL.DIPSOMANIA_SUPERCHARGER]

def REQ_DIPSOMANIA_SUPERCHARGER_TO_0(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 0 == adc[CB_CTRL.DIPSOMANIA_SUPERCHARGER]

def REQ_CHAMAEMELUM_NOBILE_TO_3(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 255 == adc[CB_CTRL.CHAMAEMELUM_NOBILE]

def REQ_CHAMAEMELUM_NOBILE_TO_2(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 182 == adc[CB_CTRL.CHAMAEMELUM_NOBILE]

def REQ_CHAMAEMELUM_NOBILE_TO_1(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 86 == adc[CB_CTRL.CHAMAEMELUM_NOBILE]

def REQ_CHAMAEMELUM_NOBILE_TO_0(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 0 == adc[CB_CTRL.CHAMAEMELUM_NOBILE]

def REQ_CONDENSER_TO_3(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 255 == adc[CB_CTRL.CONDENSER]

def REQ_CONDENSER_TO_2(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 183 == adc[CB_CTRL.CONDENSER]

def REQ_CONDENSER_TO_1(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 87 == adc[CB_CTRL.CONDENSER]

def REQ_CONDENSER_TO_0(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 0 == adc[CB_CTRL.CONDENSER]

def REQ_HERABORA_PRESSED(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.HERABORA]

# For 4 Panel
def REQ_GIPERBOLOID_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.GIPERBOLOID]

def REQ_GIPERBOLOID_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 0 == buttons[CB_CTRL.GIPERBOLOID]

def REQ_UGNETATEL_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.UGNETATEL]

def REQ_UGNETATEL_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 0 == buttons[CB_CTRL.UGNETATEL]

def REQ_TECHNO_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.TECHNO]

def REQ_TECHNO_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 0 == buttons[CB_CTRL.TECHNO]

def REQ_ZOND_JC_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.ZOND_JC]

def REQ_ZOND_JC_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 0 == buttons[CB_CTRL.ZOND_JC]

def REQ_ZOND_JS_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.ZOND_JS]

def REQ_ZOND_JS_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 0 == buttons[CB_CTRL.ZOND_JS]

