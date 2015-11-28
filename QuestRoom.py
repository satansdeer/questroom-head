from __future__ import print_function
from Parser import parse
from QuestDeviceMaster import *
from GameState import GameState
from Requirement import Requirement
from Task import Task
from Action import Action
import time
import threading
from KeyboardListener import KeyboardListener
from NewFunctions import *

clients = None

class QuestRoom(threading.Thread):

    def __init__(self, cli):
        global clients
        clients = cli
        super(QuestRoom, self).__init__()


    def run(self):
        print("quest room thread start")
        master = SpaceDeviceMaster(1)
        simSlave = master.addSlave("mainPuzzle", "/dev/tty.usbserial-A4033KK5", 1)
        simSlave2 = master.addSlave("capSlave", "/dev/tty.usbserial-AL0079CW", 1)
        init_leds = [0x000, 0x000, 0x000] * 32
        master.sendSetSmartLEDs(simSlave, init_leds)
        leds = master.getSmartLEDs(simSlave)
        setLedValue(leds, 8, [0xfff, 0x0, 0x0])
        setLedValue(leds, 9, [0xfff, 0x0, 0x0])
        setLedValue(leds, 10, [0xfff, 0x0, 0x0])
        setLedValue(leds, 11, [0xfff, 0x0, 0x0])

        relays = [1,1,1,0]
        master.sendSetRelays(simSlave2, relays)

        self.game_state = parse("quest_script.yml")
        self.game_state.device_master = master
        self.game_state.slave = simSlave
        self.game_state.quest_room = self
        self.game_state.start_game_loop(self.on_gameloop)


    def send_ws_message(self, client_id, message):
        str_id = str(client_id)
        if str_id not in clients: return
        clients[str_id]['object'].write_message(message)


    def on_gameloop(self, message):
        map(lambda client: clients[client]['object'].write_message(message), clients)


    def button_pressed(self, button_id):
        self.game_state.state['pressed_buttons'].append(button_id)
        print(self.game_state.state)
