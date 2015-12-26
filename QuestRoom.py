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

class QuestRoom(threading.Thread):

    def __init__(self, cli):
        global clients
        clients = cli
        game_state = None
        super(QuestRoom, self).__init__()

    def progress_bar_zero(self, monitorId):
        self.game_state.updateMonitorsListWithProgressBarZero(monitorId)

    def run(self):
        print("quest room thread start")
        master = DeviceMaster()
        #hallwayPort = "/dev/tty.usbserial-A4033KK5"
        #hallwayPort = "COM3"
        # "/dev/tty.usbserial-AL0079CW"
        #captainsBridgePort_1 = "COM5"
        #captainsBridgePort_2 = "COM4"
        #hallwayPuzzles = master.addSlave("hallwayPuzzles", hallwayPort, 1, boudrate=5)
        #captainsBridge_1 = master.addSlave("CB_SLAVE_1", captainsBridgePort_1, 1, boudrate=5)
        #captainsBridge_2 = master.addSlave("CB_SLAVE_2", captainsBridgePort_2, 1, boudrate=5)


        master.start()

        # init_leds = [0x000, 0x000, 0x000] * 32
        # master.setSmartLeds(hallwayPuzzles, init_leds)
        # leds = master.getSmartLeds(hallwayPuzzles).get()
        #setLedValue(leds, 8, [0xfff, 0x0, 0x0])
        #setLedValue(leds, 9, [0xfff, 0x0, 0x0])
        #setLedValue(leds, 10, [0xfff, 0x0, 0x0])
        #setLedValue(leds, 11, [0xfff, 0x0, 0x0])

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


    def send_ws_message(self, client_id, message):
        str_id = str(client_id)
        if str_id not in clients: return
        if 'progress_visible' not in message: message['progress_visible'] = true
        if 'countdown_active' not in message: message['countdown_active'] = true
        clients[str_id]['object'].write_message(message)


    def on_gameloop(self, message):
        map(lambda client: clients[client]['object'].write_message(message), clients)


    def button_pressed(self, button_id):
        self.game_state.state['pressed_buttons'].append(button_id)
        print(self.game_state.state)


