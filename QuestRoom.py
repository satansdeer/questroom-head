from __future__ import print_function
from Parser import parse
from deviceMaster.devicemaster import DeviceMaster
from GameState import GameState
from Requirement import Requirement
from Task import Task
from Action import Action
import time
import threading
import platform
if platform.system() == 'Windows':
    from KeyboardListener import KeyboardListener
from hallway_function import *
import tornado
from full_quest import *

import pygame

clients = None
master = None
class QuestRoom(threading.Thread):

    def __init__(self, cli):
        global clients
        clients = cli
        self.game_state = None
        sound_manager = None
        captainsBridge_2 = None
        pygame.mixer.init()
        self.ambient_music = pygame.mixer.Sound("game_ambient.wav")
        self.final_game_music = pygame.mixer.Sound("final_game.wav")
        self.win_music = pygame.mixer.Sound("you_win.wav")
        self.current_music = self.ambient_music

        hallwayPuzzles = None
        super(QuestRoom, self).__init__()

    def progress_bar_zero(self, monitorId):
        self.game_state.updateMonitorsListWithProgressBarZero(monitorId)

    def run(self):
        print("quest room thread start")
        global master
        master = DeviceMaster()
        #hallwayPort = "/dev/tty.usbserial-A4033KK5"
        self.hallwayPuzzles = master.addSlave("hallwayPuzzles", "COM3", 1, boudrate=5)
        self.captainsBridge_1 = master.addSlave("CB_SLAVE_1", "COM5", 2, boudrate=5)
        self.captainsBridge_2 = master.addSlave("CB_SLAVE_2", "COM4", 3, boudrate=5)

        master.start()

        self.game_state = parse("full_quest.yml")

        if platform.system() == 'Windows':
            keyboardListener = KeyboardListener(master, self.game_state)
            keyboardListener.daemon = True
            keyboardListener.start()

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
	if self.game_state is None: return

        message = {'message': [u" ({}).{}".format(x.id, x.title).encode('utf-8') for x in self.game_state.active_tasks]}
        message = tornado.escape.json_encode(message)
        try:
            if '42' in clients:
                clients['42']['object'].write_message(message)
        except:
            pass

    def toggle_skiped_task(self, task_id):
        """ Skip or unskip task from questlogic"""
        for task in self.game_state.tasks:
            if task_id == task.id:
                if task in self.game_state.skipped_tasks:
                    self.game_state.skipped_tasks.remove(task)
                else:
                    self.game_state.skipped_tasks.append(task)


    def button_pressed(self, button_id):
        self.game_state.state['pressed_buttons'].append(button_id)
        print(self.game_state.state)

    def play_robot(self, sound):
        self.sound_manager.play_sound(sound)


