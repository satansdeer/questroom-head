from __future__ import print_function
import time

start_time = time.time()

WIRE_CONNECTED = lambda state: (time.time() - start_time) > 10
ENABLE_FUSE_PUZZLE = lambda: print("Fuse puzzle enabled")

FUZE_PUZZLE_SOLVED = lambda state: (time.time() - start_time) > 12
ENABLE_RADIO = lambda: print("Radio enabled")

CORRECT_SEQUENCE_ENTERED = lambda state: (time.time() - start_time) > 13
OPEN_FIRST_BOX = lambda: print("First box opened")

MECHANICS_CARD_USED = lambda state: (time.time() - start_time) > 14
ENABLE_TUMBLER_PUZZLE = lambda: print("Tumbler puzzle enabled")

TUMBLER_PUZZLE_SOLVED = lambda state: (time.time() - start_time) > 15
OPEN_SECOND_BOX = lambda: print("Second box opened")

HIDDEN_TUMBLER_PUZZLE_SOLVED = lambda state: (time.time() - start_time) > 16
OPEN_THIRD_BOX = lambda: print("Third box opened")

COMMUTATOR_PUZZLE_SOLVED = lambda state: (time.time() - start_time) > 17
OPEN_FOURTH_BOX = lambda: print("Fourth box opened")

ROBOT_ASSEMBLED = lambda state: (time.time() - start_time) > 18
ROBOT_SAY_RIDDLE = lambda: print("Robot said riddle")

ENGINE_ASSEMBLED = lambda state: (time.time() - start_time) > 19
ACTIVATE_CAPTAIN_BRIDGE = lambda: print("Captain bridge activated")
