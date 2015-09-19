import tornado.ioloop
import tornado.httpserver
import tornado.ioloop
import config

from pymongo import MongoClient
from tornado.web import Application, url
from handlers import *


class App(Application):
    def __init__(self, **overrides):
        handlers = [
            (r"/test?", TestHandler),
            (r"/rooms?", RoomsPostHandler),
        ]

        Application.__init__(self, handlers)
        self.client = MongoClient(config.URI)


if __name__ == "__main__":
    print("starting shit")
    application = App()
    http_server = tornado.httpserver.HTTPServer(application)

    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()