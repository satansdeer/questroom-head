import os
import tornado.ioloop
import tornado.web
import tornado.websocket
from GameState import GameState
from time import sleep
from QuestRoom import QuestRoom

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)

clients = dict()

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('index.html')

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        clients[self.id] = { "id": self.id, "object": self }

    def on_message(self, message):
        self.write_message("%s: %s" % (self.id, message))
        print "Client %s received a message: %s" % (self.id, message)

    def on_close(self):
        if self.id not in clients: return
        del clients[self.id]

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
    QuestRoom(clients).start()
    print("Questroom thread started..")
    tornado.ioloop.IOLoop.instance().start()
