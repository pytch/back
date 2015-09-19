import json
import uuid
import tornado.escape
import datetime
import threading

from datetime import timedelta
from tornado.web import RequestHandler


FAILED = {"success": False}


class BaseHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD")
        self.set_header("Content-Type", "application/json")
        self.set_header("Server", "ayyyyyyy lmaooooooooooooo")


    def initialize(self):
        self.db = self.application.client['pytchapp']
        self.rooms = self.db['rooms']
        self.users = self.db['users']


    def fail(self):
        self.write(json.dumps(FAILED))


class TestHandler(BaseHandler):

    def get(self):
        self.write("lmao cat")


class AuthHandler(BaseHandler):

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        user = self.users.find_one({'email': data['email']})

        if not user:
            self.fail()
            return

        if data['password'] != user['password']:
            self.fail()
            return

        user.pop('_id')
        self.write(json.dumps(user))


class UsersHandler(BaseHandler):

    def post(self):
        user_data = tornado.escape.json_decode(self.request.body)
        user_data['id'] = uuid.uuid4().hex[:10]
        self.users.insert_one(user_data)
        self.write(json.dumps({'id': user_data['id']}))


class RoomsPostHandler(BaseHandler):

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        user_id = data['id']

        user = self.users.find_one({'id': user_id})
        print(user)

        if not user:
            self.fail()
            return

        user_data = {
            'donated': 1,
            'prize_url': '',
            'user_id':  user_id,
        }

        start_time = datetime.datetime.utcnow()
        room_id = uuid.uuid4().hex[:10]

        # generate 10 items < 1
        items = []

        room = {
            'id': room_id,
            'items': items,
            'raised': 1,
            'start_time': start_time.isoformat(),
            'users': {
                user_id: user_data
            }
        }
        self.rooms.insert_one(room)

        run_at = start_time + timedelta(hours=1)
        delay = (run_at - start_time).total_seconds()
        #threading.Timer(delay, buy_items).start()

        room.pop('_id', None)
        self.write(json.dumps(room))


class RoomsHandler(BaseHandler):

    def put(self, room_id):
        room = self.rooms.find_one({'id': room_id})
        print(room)

        if not room:
            self.fail()
            return

        data = tornado.escape.json_decode(self.request.body)
        user_id = data['id']

        user = self.users.find_one({'id': user_id})
        print(user)
        print(room)

        if not user:
            self.fail()
            return

        if user['id'] in room:
            self.fail()
            return

        user_data = {
            'donated': 1,
            'prize_url': '',
            'user_id':  user_id,
        }
        room['users'][user_id] = user_data
        room['raised'] += 1

        self.rooms.update_one({'id': room_id}, {'$set': {'users': room['users']}, '$inc': {'raised': 1}})

        room.pop('_id')
        self.write(json.dumps(room))


class PitchesHandler(BaseHandler):

    def post(self, room_id):
        room = self.rooms.find_one({'id': room_id})

        if not room:
            self.fail()
            return

        data = tornado.escape.json_decode(self.request.body)
        user_id = data['id']
        pitch = float(data['pitch'])

        user = self.users.find_one({'id': user_id})

        if not user or user_id not in room['users']:
            self.fail()
            return

        room['users'][user_id]['donated'] += pitch
        room['raised'] += pitch

        self.rooms.update_one({'id': room_id}, {'$set': {'users': room['users']}, '$inc': {'raised': pitch}})
        self.write(json.dumps(room))


def buy_items():
    pass
