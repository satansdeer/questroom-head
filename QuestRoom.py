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
#from cb_functions import *
import tornado
from full_quest import *

clients = None
master = None
class QuestRoom(threading.Thread):

    def __init__(self, cli):
        global clients
        clients = cli
        game_state = None
        sound_manager = None
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

        init_leds = [0x000, 0x000, 0x000] * 32
        master.setSmartLeds(self.hallwayPuzzles, init_leds)
        leds = master.getSmartLeds(self.hallwayPuzzles).get()
        setLedValue(leds, 8, [0x888, 0x0, 0x0])
        setLedValue(leds, 9, [0x888, 0x0, 0x0])
        setLedValue(leds, 10, [0x888, 0x0, 0x0])
        setLedValue(leds, 11, [0x888, 0x0, 0x0])
        master.setSmartLeds(self.hallwayPuzzles, leds)
        master.setRelays(self.hallwayPuzzles, [0,0,0,0])
        time.sleep(1)
        master.setRelays(self.hallwayPuzzles, [1,1,1,1])
        master.setRelays(self.captainsBridge_2, [1,1,1,0])
        keyboardListener = KeyboardListener(master)
        keyboardListener.daemon = True
        keyboardListener.start()

        self.game_state = parse("full_quest.yml")
        self.game_state.device_master = master
        self.game_state.slave = hallwayPuzzles
        self.game_state.quest_room = self
        self.game_state.start_game_loop(self.send_state)

    def set_door_state(self, door_id, door_state):
        relays = master.getRelays(self.captainsBridge_2).get()
        relays[door_id] = door_state
        master.setRelays(self.captainsBridge_2, relays)

    def set_box_state(self, box_id, box_state):
        smartLeds = master.getSmartLeds(self.hallwayPuzzles)
        if(box_state == 0):
            smartLeds.setOneLed(box_id + 8, Colors.BLUE)
        else:
            smartLeds.setOneLed(box_id + 8, Colors.RED)
        relays = master.getRelays(self.hallwayPuzzles).get()
        relays[box_id] = box_state
        master.setRelays(self.hallwayPuzzles, relays)

    def send_ws_message(self, client_id, message):
        str_id = str(client_id)
        if str_id not in clients: return
        if 'progress_visible' not in message: message['progress_visible'] = True
        if 'countdown_active' not in message: message['countdown_active'] = True
        clients[str_id]['object'].write_message(message)


    def send_state(self, message):
        message = {'message': [x.title for x in self.game_state.active_tasks]}
        message = tornado.escape.json_encode(message)
        try:
            if '42' in clients:
                clients['42']['object'].write_message(message)
        except:
            pass


    def button_pressed(self, button_id):
        self.game_state.state['pressed_buttons'].append(button_id)
        print(self.game_state.state)

    def play_robot(self):
        self.sound_manager.play_sound('full_robot.wav')


