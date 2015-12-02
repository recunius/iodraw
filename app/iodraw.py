import logging
from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
Bootstrap(app)
socketio = SocketIO(app)

room_registry = { }

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@socketio.on('draw')
def handle_draw(data):
    # TODO: validate data
    user_room = rooms()[0]
    logger.info('User room = {}'.format(user_room))
    emit('receiveDraw', data, room=user_room)

@socketio.on('joinRequest')
def handle_join_request(msg):
    logger.info('Received {}'.format(msg))
    # TODO: validate data
    join_room(msg['room'])

    # TODO: pass back current drawing (likely async, so emit instead of return)
    emit('initRoom', { 'room' : msg['room'], 'pic' : { } })

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
