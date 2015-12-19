#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import tornado.ioloop
import tornado.web
import tornado.websocket
from GameState import GameState
from time import sleep
from QuestRoom import QuestRoom
from KeyboardListener import KeyboardListener
from tornado.options import define, options, parse_command_line
import json

BUTTONS_NUM = 4

define("port", default=8888, help="run on the given port", type=int)

clients = dict()
quest_room = None

all_buttons = [
        {'title': 'Глюкало',  'id': 0},
        {'title': 'Трюндель', 'id': 1},
        {'title': 'Пресло',   'id': 2},
        {'title': 'Коковник', 'id': 3},
        {'title': 'Бедодька', 'id': 4},
        {'title': 'Сорвалец', 'id': 5},
        {'title': 'Глевло',   'id': 6},
        {'title': 'Плевло',   'id': 7},
]
used_buttons = []

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('index.html')

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        clients[self.id] = { "id": self.id, "object": self }
        data = {'msg_type': 'init', 'buttons': self.get_buttons(int(self.id)), 'hearts': 3}
        self.write_message(data)

    def on_message(self, jsonMessage):
    	message = json.loads(jsonMessage)
	#print("Id: {id}, message: {msgStr} \nclients {clients}".format(
#		id=message['id'], msgStr=message['message'], clients=clients))

        # Progress bar is zero
        if "Time end" in message['message']:
           quest_room.progress_bar_zero(message['id']
       #  if "Button clicked:" in message:
       #      button_id = message.split(':')[1]
       #      quest_room.button_pressed(button_id)


    def on_close(self):
        if self.id not in clients: return
        del clients[self.id]

    def get_buttons(self, device_id):
        return all_buttons[(device_id-1)*BUTTONS_NUM:device_id*BUTTONS_NUM]

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/socket', WebSocketHandler),
    ],
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    autoreload=True,
)

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    quest_room = QuestRoom(clients)
    quest_room.start()
    #KeyboardListener().start()
    tornado.ioloop.IOLoop.instance().start()
