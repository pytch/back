import json
import uuid
import tornado.escape
import datetime
import threading

from datetime import timedelta
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

    def post(self):
        user_data = tornado.escape.json_decode(self.request.body)
        user_data['donated'] = 0
        user_data['prize_url'] = ''
        user_data['id'] = uuid.uuid4().hex[:10]

        start_time = datetime.datetime.utcnow()
        room_id = uuid.uuid4().hex[:10]  

        room = {
            'id': room_id,
            'raised': 0,
            'start_time': start_time.isoformat(),
            'users': {
                user_data['id']: user_data
            }
        }
        self.rooms.insert_one(room)

        run_at = start_time + timedelta(hours=1)
        delay = (run_at - now).total_seconds()
        threading.Timer(delay, buy_items).start()

        room.pop('_id', None)
        self.write(json.dumps(room))


def buy_items():
    pass