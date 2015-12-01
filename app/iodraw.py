from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

app = Flask(__name__)
Bootstrap(app)
socketio = SocketIO(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@socketio.on('joinRequest', namespace='/draw')
def handle_join_request(msg):
    # TODO: validate data
    join_room(msg['room'])
    emit('joinResponse', { 'room' : msg['room'] })

if __name__ == '__main__':
    socketio.run(app, debug=True)
