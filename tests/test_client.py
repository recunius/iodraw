import logging

logging.getLogger('requests').setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

import os
import unittest
import json

from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace

logger = logging.getLogger(__name__)


# TODO: Use custom namespace. Waiting on bug socketIO-client bug:
# https://github.com/invisibleroads/socketIO-client/issues/96
class Test_Join(unittest.TestCase):
    ROOM = "test"

    def setUp(self):
        self.socketIO = SocketIO('localhost', 5000,  LoggingNamespace)
        self.socketIO.on('initRoom', self.on_init_room)

    def on_init_room(self, arg):
        logger.info("initRoom: Received {} ({})".format(arg, type(arg)))
        self.assertIsInstance(arg, dict, msg='Expected a dict')
        self.assertEqual(arg['pic'], {}, msg='Expected key pic = {}')
        self.assertEqual(arg['room'], Test_Join.ROOM, msg='Expected key room = {}'.format(Test_Join.ROOM))

    def test_requestJoin(self):
        self.socketIO.emit('joinRequest', { "room" : Test_Join.ROOM })
        self.socketIO.wait(seconds=1)

if __name__ == '__main__':
    unittest.main()

