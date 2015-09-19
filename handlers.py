import json

from tornado.web import RequestHandler    


class BaseHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD")
        self.set_header("Content-Type", "application/json")
        self.set_header("Server", "ayyyyyyy lmaooooooooooooo")


    def initialize(self):
        self.db = self.application.client['pytchapp']
        self.rooms = self.db['rooms']


class TestHandler(BaseHandler):
    def get(self):
        self.write("lmao cat")


class RoomsPostHandler(BaseHandler):
    def get(self):
        room = self.rooms.find({'id': 1})[0]
        room.pop('_id', None)
        self.write(json.dumps(room))