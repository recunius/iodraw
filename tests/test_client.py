import logging
import os
import unittest
import json
import uuid
from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace

logging.getLogger('requests').setLevel(logging.WARN)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class IODrawTestCase(unittest.TestCase):
    
    def setUp(self):
        self.socketIO = SocketIO('localhost', 5000,  LoggingNamespace)

# TODO: Use custom namespace. Waiting on bug socketIO-client bug:
# https://github.com/invisibleroads/socketIO-client/issues/96
class Test_Join(IODrawTestCase):
    ROOM = "test_join"
    
    def on_init_room(self, arg):
        logger.info("initRoom: Received {} ({})".format(arg, type(arg)))
        self.assertIsInstance(arg, dict, msg='Expected a dict')
        self.assertEqual(arg['pic'], [], msg='Expected key pic = []')
        self.assertEqual(arg['room'], Test_Join.ROOM, msg='Expected key room = {}'.format(Test_Join.ROOM))

    def test_request_join(self):
        self.socketIO.on('initRoom', self.on_init_room)
        self.socketIO.emit('joinRequest', { "room" : Test_Join.ROOM })
        self.socketIO.wait(seconds=1)

class Test_Draw(IODrawTestCase):
    # use uuid to avoid conflicts on retesting
    ROOM = "test_draw" + str(uuid.uuid4())

    def setUp(self):
        super().setUp()
        self.socket2 = SocketIO('localhost', 5000, LoggingNamespace)

    def on_receive_draw(self, line):
        logger.info("on_receive_draw: Received {}".format(line))
        self.assertIsInstance(line, dict, msg='Expected an array')
        self.assertListEqual(line['from'], [0, 0])
        self.assertListEqual(line['to'], [300, 200])

    def test_draw(self):
        self.socketIO.emit('joinRequest', { "room" : Test_Draw.ROOM })
        self.socket2.emit('joinRequest', { "room" : Test_Draw.ROOM })
        self.socketIO.wait(seconds=1)
        self.socket2.wait(seconds=1)
        self.socket2.on('receiveDraw', self.on_receive_draw)
        self.socketIO.emit('draw', {'from': [0, 0], 'to': [ 300, 200 ] })
        self.socketIO.wait(seconds=1)
        self.socket2.wait(seconds=1)

class Test_Join_Existing_Room(IODrawTestCase):
    # use uuid to avoid conflicts on retesting
    ROOM = "test_join_existing-" + str(uuid.uuid4())

    def setUp(self):
        super().setUp()
        self.socket2 = SocketIO('localhost', 5000, LoggingNamespace)

    def on_init_room(self, data):
        logger.info("on_init_room: Received {} ({})".format(data, type(data)))
        self.assertIsInstance(data, dict, msg='Expected a dict')
        self.assertEqual(len(data['pic']), 1, msg='Expected key pic {} to be of len(1)'.format(data['pic']))
        self.assertListEqual(data['pic'][0]['from'], [0, 0])
        self.assertListEqual(data['pic'][0]['to'], [300, 200])

    def test_draw(self):
        self.socketIO.emit('joinRequest', { "room" : Test_Join_Existing_Room.ROOM })
        self.socketIO.wait(seconds=1)
        self.socketIO.emit('draw', {'from': [0, 0], 'to': [ 300, 200 ] })
        self.socketIO.wait(seconds=1)
        self.socket2.wait(seconds=1)
        self.socket2.on('initRoom', self.on_init_room)
        self.socket2.emit('joinRequest', { "room" : Test_Join_Existing_Room.ROOM })
        self.socket2.wait(seconds=1)

if __name__ == '__main__':
    unittest.main()

