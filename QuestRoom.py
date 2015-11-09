from __future__ import print_function
from Parser import parse
from QuestDeviceMaster import *
from GameState import GameState
from Requirement import Requirement
from Stage import Stage
from Action import Action
import time
import threading

clients = None

class QuestRoom(threading.Thread):

    def __init__(self, cli):
        global clients
        clients = cli
        super(QuestRoom, self).__init__()

    def run(self):
        print("quest room thread start")
        master = SpaceDeviceMaster()
        simSlave = True
        #simSlave = master.addSlave("simSlave1", "/dev/tty.Bluetooth-Modem", 1)

        print(clients)
        game_state = parse("script.yml")
        game_state.master = master
        game_state.state = True
        game_state.slave = simSlave
        game_state.start_game_loop(self.on_gameloop)

    def on_gameloop(self, message):
        map(lambda client: clients[client]['object'].write_message(message), clients)
