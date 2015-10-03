from __future__ import print_function
from QuestDeviceMaster import *
from GameState import GameState
from Requirement import Requirement
from Stage import Stage
from Action import Action

master = SpaceDeviceMaster()

simSlave = master.addSlave("simSlave1", "/dev/tty.usbserial-A4033KK5", 1)

master.sendConnectionCheck("simSlave1")

requirement = Requirement()
state = master.getButtons(simSlave)
print(state)
requirement.state = state
requirement.validation_function = lambda state: state[6] == 0

action = Action()
action.function_to_perform = lambda: master.sendSetSimpleLEDs(simSlave, [1, 0]*40)

action_2 = Action()
action_2.function_to_perform = lambda: print("All actions performed")

first_stage = Stage()
first_stage.add_action(action)
first_stage.add_action(action_2)
first_stage.add_requirement(requirement)

game = GameState()
game.add_stage(first_stage)

game.start_game_loop()

