import logging
from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from drawings import Drawings

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

MAX_ACTIVE_DRAWINGS = 5

app = Flask(__name__)
Bootstrap(app)
socketio = SocketIO(app)

drawings = Drawings(MAX_ACTIVE_DRAWINGS)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@socketio.on('draw')
def handle_draw(line):
    """Append line to drawing in cache and emit line to all users in room"""
    # TODO: validate line
    user_room = rooms()[0]
    drawings.get_drawing(user_room).append(line)
    emit('receiveDraw', line, room=user_room)

@socketio.on('joinRequest')
def handle_join_request(data):
    """Add user to given room"""
    logger.info('Received {}'.format(data))
    # TODO: validate data

    room = data['room']
    join_room(room)

    pic = drawings.get_drawing(room)
    emit('initRoom', { 'room' : data['room'], 'pic' : pic })

@socketio.on('leaveRequest')
def handle_leave_request(data):
    """Remove user from given room"""
    logger.info('Received {}'.format(data))
    leave_room(data['room'])
    emit('leaveRoom')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
