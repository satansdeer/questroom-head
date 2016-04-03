#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import tornado.ioloop
import tornado.web
import tornado.websocket
from GameState import GameState
from time import sleep
from SoundManager import SoundManager
from QuestRoom import QuestRoom

import platform
if platform.system() == 'Windows':
    from KeyboardListener import KeyboardListener
from tornado.options import define, options, parse_command_line
import json

BUTTONS_NUM = 4

define("port", default=8888, help="run on the given port", type=int)

clients = dict()
quest_room = None
sound_manager = None
keyboard_listener = None

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


class DashboardHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('dashboard.html')


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        if self.id in clients:
            del clients[self.id]
        clients[self.id] = { "id": self.id, "object": self }

        id_str = str(self.id)
        # print("quest last_sended_messages: {}".format(quest_room.last_sended_messages))

        init_data = {'init': 'True'}
        self.write_message(init_data)

        if id_str in quest_room.last_sended_messages:
            last_data = quest_room.last_sended_messages[id_str]
            self.write_message(last_data)

        quest_room.send_state(None)

    def on_message(self, jsonMessage):
        message = json.loads(jsonMessage)
        print(message)
        print(message['message'])
        if "Time end" in message['message']:
            # pass
            print("We receive: {} and {}".format(message['message'], message['id']))
            quest_room.progress_bar_zero(message['id'])
        if "play_sound" == message['message']:
            sound_id = message['sound']
            sound_manager.play_sound(sound_id)
        if "door" == message['message']:
            door_id = int(message['door_id'])
            door_state = message['state']
            quest_room.set_door_state(door_id, door_state)
        if "box" == message['message']:
            box_id = int(message['box_id'])
            box_state = message['state']
            quest_room.set_box_state(box_id, box_state)
        if "get_state" == message['message']:
            quest_room.send_state()
        if "skip_task" in message['message']:
            if message['task_id'].isdigit():
                task_id = int(message['task_id'])
                quest_room.toggle_skiped_task(task_id)

        if "light" == message['message']:
            quest_room.turn_light(message['light_id'])

        if "set_room_light" == message['message']:
            room_led = message['room_led_id']
            rgb_color_str = message['color']
            rgb_color = [int(char_h + char_l, 16) for char_h, char_l in zip(rgb_color_str[0::2], rgb_color_str[1::2])]
            # print("We receive set_room_light with room_led_id: {} and color {} = {}".format(room_led, rgb_color_str, rgb_color))

            quest_room.set_room_light(room_led, rgb_color)



    def on_close(self):
        if self.id not in clients: return
        del clients[self.id]

    def get_buttons(self, device_id):
        return all_buttons[(device_id-1)*BUTTONS_NUM:device_id*BUTTONS_NUM]

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/dashboard', DashboardHandler),
    (r'/socket', WebSocketHandler),
    ],
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    autoreload=True,
)

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    sound_manager = SoundManager()
    sound_manager.daemon = True
    sound_manager.start()
    quest_room = QuestRoom(clients)
    quest_room.sound_manager = sound_manager
    quest_room.start()
    tornado.ioloop.IOLoop.instance().start()
