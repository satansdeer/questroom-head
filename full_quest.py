#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import time
import random
from Radio import Radio
from collections import Counter
from copy import copy
start_time = time.time()

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

    #    # ADC
    CHAMAEMELUM_NOBILE = 0
    DIPSOMANIA_SUPERCHARGER = 1
    HYPER_DRIVE_GENERATOR = 2
    CONDENSER = 7

    DOOR_ENTER = 1
    DOOR_ENGINE = 2
    DOOR_CAPTAIN = 3

class Colors:
    WHITE = [0xff, 0xff, 0xff]
    RED = [0xfff, 0x0, 0x0]
    LIGHT_RED = [0xff, 0x33, 0x33]
    GREEN = [0x0, 0xff, 0x0]
    LIGHT_GREEN = [0x33, 0xff, 0x33]
    BLUE = [0x0, 0x0, 0xff]
    NONE = [0x0, 0x0, 0x0]

class AdcIdTable:
    RADIO = 0
    BOX_LOCK = 1


def setLedValue(leds, id, color):
    leds[id * 3 + 0] = color[0]
    leds[id * 3 + 1] = color[1]
    leds[id * 3 + 2] = color[2]


def REQ_WIRE_CONNECTED(master, task, game_state):
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


def AC_ENABLE_FUSE_PUZZLE(master, task, game_state):
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    # smartLeds.setOneLed(LedsIdTable.FUSE, Colors.RED)

    fuseConnection = master.getButtons(hallwayPuzzles).get()[
        ButtonsIdTable.FUSE]
    if fuseConnection:
        smartLeds.setOneLed(LedsIdTable.FUSE, Colors.GREEN)
    else:
        smartLeds.setOneLed(LedsIdTable.FUSE, Colors.RED)
def AC_DISABLE_FUSE_PUZZLE(master, task, game_state):
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.FUSE, [0x0, 0x0, 0x0])


def REQ_FUSE_PUZZLE_SOLVED(master, task, game_state):
    buttons = master.getButtons(hallwayPuzzles)
    fuseSolved = buttons.get()[ButtonsIdTable.FUSE]
    if fuseSolved:
        smartLeds = master.getSmartLeds(hallwayPuzzles)
        smartLeds.setOneLed(LedsIdTable.FUSE, Colors.LIGHT_GREEN)
        return True
    return False


def REQ_FUSE_REMOVED(master, task, game_state):
    buttons = master.getButtons(hallwayPuzzles)
    fuseSolved = buttons.get()[ButtonsIdTable.FUSE]
    if not (fuseSolved == 1 ):
        return True
    return False

radio = 0

def AC_ENABLE_RADIO(master, task, game_state):
    global radio
    print("Radio puzzle solved")
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.BOX_1, Colors.RED)

    radio = Radio(0.5, 0.001)
    sounds = [('harp.wav',40.0,80.0), ('island_music_x.wav',120.0,160.0), ('leftright_final.wav',200.0,240.0)]
    radio.init_sounds(sounds, 'noize.wav')
    radio.start()

    game_state.add_active_task_with_id(12)


def REQ_RADIO_BROADCAST(master, task, game_state):
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


def AC_ADD_CONNECT_WIRE(master, task, game_state):
    game_state.add_active_task_with_id(TaskIdTable.WIRE_CONNECTED)


def AC_ADD_DISCONNECT_WIRE(master, task, game_state):
    game_state.add_active_task_with_id(TaskIdTable.WIRE_DISCONNECTED)


def AC_ADD_FUSE_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(TaskIdTable.FUSE_PUZZLE)

def AC_ADD_FUSE_REMOVED(master, task, game_state):
    game_state.add_active_task_with_id(TaskIdTable.FUSE_REMOVED)

# Включение и Выкл.  радио выполняются в action
# def ADD_DISABLE_RADIO(master, task, game_state):
#     game_state.add_active_task_with_id(3)


def AC_ADD_SEQUENCE_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(4)


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


def AC_ADD_ENGINE_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(11)

def AC_ADD_BATTARIES_PUZZLE(master, task, game_state):
    game_state.add_active_task_with_id(13)

def AC_ADD_ACTIVATE_CAPTAIN_BRIDGE(mastre, task, game_state):
    game_state.add_active_task_with_id(13)
#===========================================================


def REQ_SECRET_DOORS(master, task, game_state):
    # buttonStartPosition = 17
    return False
    buttons = master.getButtons(hallwayPuzzles).get()[12:18]
    if buttons[3:6] == [0, 1, 0]:
        relays = buttons[0:3]
        relays.insert(0, 0)
        master.setRelays(captainsBridge, relays)
    # master.sendGetButtons(slavePuzzle)
    return False


# def HIDDEN_TUMBLER_PUZZLE_SOLVED(master, task, game_state):
#     smartLeds = master.getSmartLeds(hallwayPuzzles).get()
#
#     ledIdStartPosition = 0
#     buttonStartPosition = 0
#     buttons = master.getButtons(hallwayPuzzles).get()
#     # print("---Time before true {:.3} seconds ---".format(time.time() - start_time))
#
#     for index in range(6):
#         buttonIndex = buttonStartPosition + index
#         ledID = ledIdStartPosition + index
#         if buttons[buttonIndex]:
#             setLedValue(smartLeds, ledID, Colors.BLUE)
#         else:
#             setLedValue(smartLeds, ledID, Colors.RED)
#
#     master.setSmartLeds(hallwayPuzzles, smartLeds)
#
#     if buttons[0:6] == [1] * 6:
#         return True
#     return False

def AC_OPEN_FIRST_BOX(master, task, game_state):
    print("First box was open!")
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    # blue, because blue and green are switched
    smartLeds.setOneLed(LedsIdTable.BOX_1, Colors.BLUE)
    relays = master.getRelays(hallwayPuzzles).get()
    relays[0] = 1
    master.setRelays(hallwayPuzzles, relays)

def AC_OPEN_SECOND_BOX(master, task, game_state):
    print("Second box was open!")
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.BOX_2, Colors.BLUE)

    
    relays = master.getRelays(hallwayPuzzles).get()
    relays[1] = 1
    master.setRelays(hallwayPuzzles, relays)


def AC_OPEN_THIRD_BOX(master, task, game_state):
    time.sleep(3)
    print("Third box was open!")
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.BOX_3, Colors.BLUE)

    relays = master.getRelays(hallwayPuzzles).get()
    relays[2] = 1
    master.setRelays(hallwayPuzzles, relays)


def AC_OPEN_FOURTH_BOX(master, task, game_state):
    print("Fourth box was open!")
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.BOX_4, Colors.BLUE)

    relays = master.getRelays(hallwayPuzzles).get()
    relays[3] = 1
    master.setRelays(hallwayPuzzles, relays)




def REQ_COMMUTATOR_PUZZLE_SOLVED(master, task, game_state):
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
# def REQ_TUMBLER_PUZZLE_SOLVED(master, task, game_state):
#
#     smartLeds = master.getSmartLeds(hallwayPuzzles).get()
#     ledIdStartPosition = 31
#     buttonStartPosition = 17
#     buttons = master.getButtons(hallwayPuzzles).get()
#
#     for index in range(6):
#         buttonIndex = buttonStartPosition - index
#         ledID = ledIdStartPosition - index
#         if buttons[buttonIndex]:
#             setLedValue(smartLeds, ledID, Colors.BLUE)
#         else:
#             setLedValue(smartLeds, ledID, Colors.RED)
#
#     master.setSmartLeds(hallwayPuzzles, smartLeds)
#
#     if buttons[12:18] == [1] * 6:
#         return True
#     return False


def AC_DISABLE_RADIO(master, task, game_state):
    radio.stop()
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

lastLockPosition = 0
state = 0
# массив значений
READ_DATA_STACK = []
# максимальная длина массива, после достижение которой массив сброситься
READ_DATA_STACK_LENGTH = 180*5


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
PLAYER_SEQUENCE=[]

def REQ_CORRECT_SEQUENCE_ENTERED(master, task, game_state):
    # return True
    # Сохраняем последнее выбранное значение
    global lastLockPosition, state
    global PLAYER_SEQUENCE
    global READ_DATA_STACK, READ_DATA_STACK_LENGTH
    # Позиция в массиве ADC
    LOCK_ID = 1
    # погрешность
    ERROR_VALUE = 15

    # ACTIVATION_SEQUENCE = ['L', 'L', 'R', 'L', 'R', 'R', 'L', 'R']
    # Последовательность для открытия
    # L - влево; R - вправо
    ACTIVATION_SEQUENCE = ['L','L', 'L', 'R', 'L']
    # time.sleep(0.6)

    value = master.getAdc(hallwayPuzzles).get()[LOCK_ID]
    READ_DATA_STACK.append(value)

    if len(READ_DATA_STACK) < READ_DATA_STACK_LENGTH:
        return


    result = READ_DATA_STACK[0]
    for val in READ_DATA_STACK[1:]:
        if abs(val - result) > 5:
            READ_DATA_STACK = []
            return
        result = val


    PLAYER_SEQUENCE = PLAYER_SEQUENCE[:len(ACTIVATION_SEQUENCE)]
    # get most freq value
    value = Counter(READ_DATA_STACK).most_common(1)[0][0]
    READ_DATA_STACK = []

    lockPosition = value
    # print("Lock value: {}".format(value))
    # if (lockPosition != lastLockPosition):
        # print("LastValue: {}, newValue: {}, state: {} {}".format(
        # lastLockPosition, lockPosition, state, ACTIVATION_SEQUENCE[state - 1]))

    # Смотрим, менялась ли позиция переключателя.
    lessDefault = lastLockPosition < (lockPosition + ERROR_VALUE)
    largeDefault = lastLockPosition > (lockPosition - ERROR_VALUE)
    if lessDefault and largeDefault:
        lastLockPosition = lockPosition
        return False


    turnDirection = turn(lastLockPosition, lockPosition)
    PLAYER_SEQUENCE.insert(0, turnDirection)



    reversePlayerSequence = copy(PLAYER_SEQUENCE[:len(ACTIVATION_SEQUENCE)])
    reversePlayerSequence.reverse()
    print("Player sequence: {} \n reverse: {}".format(PLAYER_SEQUENCE, reversePlayerSequence))

    if ACTIVATION_SEQUENCE == reversePlayerSequence:
        print("We opened lock box: sleep!!!")
        PLAYER_SEQUENCE = []
        return  True 

    lastLockPosition = lockPosition


def REQ_MECHANICS_CARD_USED(master, task, game_state):
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


def REQ_ROBOT_ASSEMBLED(master, task, game_state):
    buttons = master.getButtons(hallwayPuzzles)
    robbotAssembled = buttons.get()[ButtonsIdTable.ROBOT_HEAD]
    game_state.quest_room.play_robot()
    if robbotAssembled:
        smartLeds = master.getSmartLeds(hallwayPuzzles)
        smartLeds.setOneLed(LedsIdTable.ROBOT_BODY_LEFT, Colors.GREEN)
        smartLeds.setOneLed(LedsIdTable.ROBOT_BODY_RIGHT, Colors.RED)
        smartLeds.setOneLed(LedsIdTable.ROBOT_HEAD, Colors.WHITE)
        return True
    return False


def AC_ROBOT_SAY_RIDDLE(master, task, game_state):
    smartLeds = master.getSmartLeds(hallwayPuzzles)
    smartLeds.setOneLed(LedsIdTable.ROBOT_BODY_LEFT, Colors.GREEN)
    smartLeds.setOneLed(LedsIdTable.ROBOT_BODY_RIGHT, Colors.RED)
    smartLeds.setOneLed(LedsIdTable.ROBOT_HEAD, Colors.WHITE)
    print("Robot say RIDDLE!")


def REQ_ENGINE_ASSEMBLED(master, task, game_state):
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


def AC_ACTIVATE_CAPTAIN_BRIDGE(master, state):
    print("Captain bridge activated")


class MESSAGE:
    BATTERY_AVALIABLE = "Battery {id} is inserted"
    BATTERY_ABSENT = "ERROR: Battery {id} missing!"
    ENGINE_BROKEN = "Repair engine"
    PRESS_HERABORA = "When you're ready press HERABORA"
    WINNER = "You're winner! Entered door are open"
    FAIL = "You're fail! Entered door are open"

def REQ_TRUE(master, task, game_state):
    return True
def AC_INIT(master, task, game_state):
    taskList = [151, 152, 153, 154, 102, 101]
    for taskId in taskList:
        game_state.add_active_task_with_id(taskId)

# def REQ_ENGINE_ASSEMBLED(master, task, game_state):
#     buttons = master.getButtons(hallwayPuzzles).get()
#     engine = buttons[ButtonsIdTable.ENGINE]
#     return engine

def AC_SHOW_ENGINE_MESSAGE(master, task, game_state):
    if REQ_ENGINE_ASSEMBLED(master, None, game_state):
        return

    for monitorId in range(1,5):
        game_state.quest_room.send_ws_message(str(monitorId), {'message': MESSAGE.ENGINE_BROKEN})

def AC_ADD_4_BATTARIES_TASKS(master, task, game_state):
    # Add req all batteries
    game_state.add_active_task_with_id(101)
    # One by one 
    game_state.add_active_task_with_id(151)
    game_state.add_active_task_with_id(152)
    game_state.add_active_task_with_id(153)
    game_state.add_active_task_with_id(154)


def REQ_CHECK_BATTERIES(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    battery_1 = buttons[CB_CTRL.BATTERY_1]
    battery_2 = buttons[CB_CTRL.BATTERY_2]
    battery_3 = buttons[CB_CTRL.BATTERY_3]
    battery_4 = buttons[CB_CTRL.BATTERY_4]
    # print("REQ_CHECK_BATTARIES")
    batteryState = (battery_1 and battery_2 and battery_3 and battery_4)

    if not batteryState:
        return batteryState

    taskList = [151, 152, 153, 154]
    for taskId in taskList:
        task = game_state.find_task_with_id(taskId)
        print("Task for delete from check_battaries: {}".format(task)) 
        print("Task for delete from check_battaries: {}".format(task.id)) 
        game_state.remove_active_task(task)
    return True

def sendBatteryMessage(game_state, monitorId, battery, batteryId):
    if battery:
        game_state.quest_room.send_ws_message(str(monitorId), {'message': MESSAGE.BATTERY_AVALIABLE.format(id=batteryId)})
    else:
        game_state.quest_room.send_ws_message(str(monitorId), {'message': MESSAGE.BATTERY_ABSENT.format(id=batteryId)})

def REQ_CHECK_BATTERY_1(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    battery = buttons[CB_CTRL.BATTERY_1]

    monitorId = game_state.getMonitorIdByTask(task)

    batteryId = 1

    sendBatteryMessage(game_state, monitorId, battery, batteryId)
    return False

def REQ_CHECK_BATTERY_2(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    battery = buttons[CB_CTRL.BATTERY_2]
    print("Task Battery_2: {}".format(task))
    print("Task Battery_2: {}".format(task.title))

    monitorId = game_state.getMonitorIdByTask(task)

    batteryId = 2

    sendBatteryMessage(game_state, monitorId, battery, batteryId)
    return False

def REQ_CHECK_BATTERY_3(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    battery = buttons[CB_CTRL.BATTERY_3]

    monitorId = game_state.getMonitorIdByTask(task)

    batteryId = 3

    sendBatteryMessage(game_state, monitorId, battery, batteryId)
    return False

def REQ_CHECK_BATTERY_4(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    battery = buttons[CB_CTRL.BATTERY_4]

    monitorId = game_state.getMonitorIdByTask(task)

    batteryId = 4

    sendBatteryMessage(game_state, monitorId, battery, batteryId)
    return False

def AC_PRESS_HERABORA(master, task, game_state):
    for monitorId in range(1,5):
        game_state.quest_room.send_ws_message(str(monitorId), {'message': MESSAGE.PRESS_HERABORA})
    # added REQ_CHECK_HERABORA task
    game_state.add_active_task_with_id(201)

def REQ_CHECK_HERABORA(master, task, game_state):
        heraboraPressed = master.getButtons(CB_SLAVE_2).get()[12]
        #print("Herabora value: {}\n", heraboraPressed)
        return heraboraPressed

def AC_CB_ADD_RANDOM_TASK(master, task, game_state):

        avaliableTaskIds = game_state.getAvaliableCBTaskIds()
        print("len avaliableTasksid = {}".format(len(avaliableTaskIds)))
        if len(avaliableTaskIds) == 0:
                return


        # check if task already true - than we don't need execute
        randomTaskRequirement = True
        while randomTaskRequirement:
            randomId = random.randint(0, len(avaliableTaskIds) -1)
            # print("avaliable task with random id {}".format(avaliableTaskIds[randomId]))

            randomTaskId = avaliableTaskIds[randomId]
            randomTask = game_state.find_task_with_id(randomTaskId)
            randomTaskRequirement = randomTask.success_requirements_satisfied(master, randomTask, game_state)

        game_state.add_active_task_with_id(randomTaskId)

        game_state.update_used_task_ids_list(randomTaskId)

def AC_ADD_END_GAME_TASK(master, task, game_state):
        game_state.add_active_task_with_id(203)

def REQ_AMOUNT_OF_TASK_SUCCESSED(master, task, game_state):
    if game_state.successfullTasksForWin == game_state.successfullTasksCounter:
            return True
    return False

def AC_ENTERED_DOOR_OPEN(master, task, game_state):
    print("Entered door opened")

def AC_SHOW_SUCCESS_MESSAGE(master, task, game_state):
    print("You are WINNER!")

    for monitorId in range(1,5):
        game_state.quest_room.send_ws_message(str(monitorId), {'message': MESSAGE.WINNER})

    time.sleep(3)
    relays = master.getRelays(CB_SLAVE_2).get()
    relays[CB_CTRL.DOOR_ENTER] = 0
    master.setRelays(CB_SLAVE_2, relays)

def REQ_AMOUNT_OF_TASK_FAILURE(master, task, game_state):
    if game_state.failureTasksForLose == game_state.failureTasksCounter:
            return True
    return False

def AC_SHOW_FAILURE_MESSAGE(master, task, game_state):

    for monitorId in range(1,5):
        game_state.quest_room.send_ws_message(str(monitorId), {'message': MESSAGE.FAIL})

    print("You lose")
    time.sleep(3)
    relays = master.getRelays(CB_SLAVE_2).get()
    relays[CB_CTRL.DOOR_ENTER] = 0
    master.setRelays(CB_SLAVE_2, relays)

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
