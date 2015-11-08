#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from Parser import parse
from QuestDeviceMaster import *
from GameState import GameState
from Requirement import Requirement
from Stage import Stage
from Action import Action
import time

master = SpaceDeviceMaster(2)
#
# simSlave = master.addSlave("simSlave1", "/dev/tty.usbserial-A4033KK5", 1)
simSlave = master.addSlave("mainPuzzle", "/dev/ttyUSB0", 1)
slaveCap = master.addSlave("Captain's bridge", "/dev/ttyUSB1", 1)
# simSlave = master.addSlave("simSlave1", "/dev/tty.usbserial-AL0079CW", 1)
#simSlave = master.addSlave("simSlave1", "/dev/tty.usbserial-AL0079CW", 1)
#
#master.sendConnectionCheck("simSlave1")
#master.COM_READ_TIMEOUT = 0
#
# while True:
#    master.sendSetSmartLEDs(simSlave, [0x000, 0x000, 0x030] * 32)
#    master.sendSetSmartLEDs(simSlave, [0x000, 0x030, 0x000] * 32)
#    time.sleep(1)
# i = 0
#master.sendSetRelays(simSlave, [0,0,0,0])
#master.sendSetRelays(simSlave, [1,1,1,1])

leds = [0x000, 0x000, 0x000] * 32
# leds[8*3:10*3] = [0xfff, 0x000, 0x000]*3
def setLed(leds, ledID): leds[ledID*3 + 0] = 0xfff; leds[ledID*3 + 1] = 0x0; leds[ledID*3 + 2] = 0x0;
setLed(leds, 8)
setLed(leds, 9)
setLed(leds, 10)
setLed(leds, 11)
master.sendSetSmartLEDs(simSlave, leds)
master.sendGetStuckButtons(simSlave)
master.sendGetStuckButtons(simSlave)
master.sendSetRelays(simSlave, [0, 0, 0, 0])
# closed Engine Door
master.sendSetRelays(slaveCap, [0, 0, 1, 0])
time.sleep(4)
print("Buttons: ", master.getButtons(simSlave))
print ("Connetction: ", master.connection("mainPuzzle"))

game_state = parse("script.yml")
game_state.device_master = master
game_state.slave = simSlave
game_state.start_game_loop()

time.sleep(12)

if False:
    requirement = Requirement()
#    state = master.getButtons(simSlave)
#    print(state)
    state = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    requirement.state = state
    requirement.validation_function = lambda state: state[6] == 0

    action = Action()
    #action.function_to_perform = lambda: master.sendSetSimpleLEDs(simSlave, [1, 0]*40)
    action.function_to_perform = lambda: print("action_1")

    action_2 = Action()
    #action_2.function_to_perform = lambda: master.sendSetSmartLEDs(simSlave, [0xccc, 0x000, 0xfff] * 32)
    action_2.function_to_perform = lambda: print("action_2")

    action_3 = Action()
    #action_3.function_to_perform = lambda: master.sendSetSmartLEDs(simSlave, [0xccc, 0x000, 0x000] * 32)
    action_3.function_to_perform = lambda: print("action_3")

    first_stage = Stage()
    first_stage.add_action(action)
    first_stage.add_action(action_2)
    first_stage.add_action(action_3)
    first_stage.add_requirement(requirement)

    second_stage_action = Action()
    #second_stage_action.function_to_perform = lambda: master.sendSetSmartLEDs(simSlave, [0x000, 0xccc, 0x000] * 32)
    second_stage_action.function_to_perform = lambda: print("stage2_action_1")

    second_stage = Stage()
    second_stage.add_action(second_stage_action)
    second_stage.add_requirement(requirement)

    game = GameState()
    game.add_stage(first_stage)
    game.add_stage(second_stage)

    game.start_game_loop()

