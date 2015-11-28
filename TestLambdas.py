#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import time

start_time = time.time()

WIRE_CONNECTED = lambda master, state: (time.time() - start_time) > 10
ENABLE_FUSE_PUZZLE = lambda master, state: print("Fuse puzzle enabled")

FUZE_PUZZLE_SOLVED = lambda master, state: (time.time() - start_time) > 12
ENABLE_RADIO = lambda master, state: print("Radio enabled")

CORRECT_SEQUENCE_ENTERED = lambda master, state: (time.time() - start_time) > 13
OPEN_FIRST_BOX = lambda master, state: print("First box opened")

MECHANICS_CARD_USED = lambda master, state: (time.time() - start_time) > 14
ENABLE_TUMBLER_PUZZLE = lambda master, state: print("Tumbler puzzle enabled")

TUMBLER_PUZZLE_SOLVED = lambda master, state: (time.time() - start_time) > 15
OPEN_SECOND_BOX = lambda master, state: print("Second box opened")

HIDDEN_TUMBLER_PUZZLE_SOLVED = lambda master, state: (time.time() - start_time) > 16
OPEN_THIRD_BOX = lambda master, state: print("Third box opened")

COMMUTATOR_PUZZLE_SOLVED = lambda master, state: (time.time() - start_time) > 17
OPEN_FOURTH_BOX = lambda master, state: print("Fourth box opened")

ROBOT_ASSEMBLED = lambda master, state: (time.time() - start_time) > 18
ROBOT_SAY_RIDDLE = lambda master, state: print("Robot said riddle")

ENGINE_ASSEMBLED = lambda master, state: (time.time() - start_time) > 19
ACTIVATE_CAPTAIN_BRIDGE = lambda master, state: print("Captain bridge activated")
