from __future__ import print_function
from Parser import parse
# from QuestDeviceMaster import *
from deviceMaster.devicemaster import DeviceMaster
from GameState import GameState
from Requirement import Requirement
from Task import Task
from Action import Action
import time
import threading
from KeyboardListener import KeyboardListener
#from NewFunctions_map import *
from hallway_function import *
from cb_functions import *

clients = None
master = None

class QuestRoom(threading.Thread):

    def __init__(self, cli):
        global clients
        clients = cli
        game_state = None
        captainsBridge_2 = None
        hallwayPuzzles = None
        super(QuestRoom, self).__init__()

    def progress_bar_zero(self, monitorId):
        self.game_state.updateMonitorsListWithProgressBarZero(monitorId)

    def run(self):
        print("quest room thread start")
        global master
        master = DeviceMaster()
        #hallwayPort = "/dev/tty.usbserial-A4033KK5"
        hallwayPort = "COM3"
        # "/dev/tty.usbserial-AL0079CW"
        captainsBridgePort_1 = "COM5"
        captainsBridgePort_2 = "COM4"
        self.hallwayPuzzles = master.addSlave("hallwayPuzzles", hallwayPort, 1, boudrate=5)
        self.captainsBridge_1 = master.addSlave("CB_SLAVE_1", captainsBridgePort_1, 1, boudrate=5)
        self.captainsBridge_2 = master.addSlave("CB_SLAVE_2", captainsBridgePort_2, 1, boudrate=5)


        master.start()
        master.setRelays(self.captainsBridge_2, [1,1,1,1])

        init_leds = [0x000, 0x000, 0x000] * 32
        master.setSmartLeds(self.hallwayPuzzles, init_leds)
        leds = master.getSmartLeds(self.hallwayPuzzles).get()
        setLedValue(leds, 8, [0x888, 0x0, 0x0])
        setLedValue(leds, 9, [0x888, 0x0, 0x0])
        setLedValue(leds, 10, [0x888, 0x0, 0x0])
        setLedValue(leds, 11, [0x888, 0x0, 0x0])
        master.setSmartLeds(self.hallwayPuzzles, leds)
        master.setRelays(self.hallwayPuzzles, [0,0,0,0])

        # relays = [1,1,1,0]
        # master.setRelays(captainsBridge, relays)
        # keyboardListener = KeyboardListener(master)
        # keyboardListener.start()

        #self.game_state = parse("cb_quest.yml")
        self.game_state = parse("hallway_quest.yml")

        #self.game_state = parse("quest_script.yml")
        self.game_state.device_master = master
        self.game_state.slave = hallwayPuzzles
        self.game_state.quest_room = self
        self.game_state.start_game_loop(self.on_gameloop)

    def set_door_state(self, door_id, door_state):
        relays = master.getRelays(self.captainsBridge_2).get()
        relays[door_id] = door_state
        master.setRelays(self.captainsBridge_2, relays)

    def set_box_state(self, box_id, box_state):
        smartLeds = master.getSmartLeds(self.hallwayPuzzles)
        if(box_state == 1):
            smartLeds.setOneLed(box_id + 8, Colors.BLUE)
        else:
            smartLeds.setOneLed(box_id + 8, Colors.RED)
        relays = master.getRelays(self.hallwayPuzzles).get()
        relays[box_id] = box_state
        master.setRelays(self.hallwayPuzzles, relays)

    def send_ws_message(self, client_id, message):
        str_id = str(client_id)
        if str_id not in clients: return
        if 'progress_visible' not in message: message['progress_visible'] = true
        if 'countdown_active' not in message: message['countdown_active'] = true
        clients[str_id]['object'].write_message(message)


    def on_gameloop(self, message):
        #map(lambda client: clients[client]['object'].write_message(message), clients)
        clients[42]['object'].write_message(message)


    def button_pressed(self, button_id):
        self.game_state.state['pressed_buttons'].append(button_id)
        print(self.game_state.state)


