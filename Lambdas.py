# -*- coding: utf-8 -*-
from __future__ import print_function

# Повторяющиеся функции:
FIRST_TUMBLER_ON = lambda state: True
TURN_FIRST_LED_GREEN = lambda: print ("FIRST led green was turned")

WIRE_CONNECTED = lambda state: True# state[11] == 1
ENABLE_FUSE_PUZZLE = lambda: print("Fuse puzzle enabled")
ENABLE_FUSE_PUZZLE2 = lambda: print("Fuse puzzle 2 enabled")

FUZE_PUZZLE_SOLVED = lambda state: True
ENABLE_RADIO = lambda: print("Radio enabled")

CORRECT_SEQUENCE_ENTERED = lambda state: True
OPEN_FIRST_BOX = lambda: print("First box opened")

MECHANICS_CARD_USED = lambda state: True
ENABLE_TUMBLER_PUZZLE = lambda: print("Tumbler puzzle enabled")

TUMBLER_PUZZLE_SOLVED = lambda state: True
OPEN_SECOND_BOX = lambda: print("Second box opened")

HIDDEN_TUMBLER_PUZZLE_SOLVED = lambda state: True
OPEN_THIRD_BOX = lambda: print("Third box opened")

COMMUTATOR_PUZZLE_SOLVED = lambda state: True
OPEN_FOURTH_BOX = lambda: print("Fourth box opened")

ROBOT_ASSEMBLED = lambda state: True
ROBOT_SAY_RIDDLE = lambda: print("Robot said riddle")

ENGINE_ASSEMBLED = lambda state: True
ACTIVATE_CAPTAIN_BRIDGE = lambda: print("Captain bridge activated")
