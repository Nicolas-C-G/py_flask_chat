from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins='*')  # Initialize SocketIO instance

# In-memory storage for rooms and messages (replace with database in production)
rooms = {}
messages = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    if room not in rooms:
        rooms[room] = []
    emit('room_info', {'room': room, 'messages': rooms[room]}, room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    username = data['username']
    message = data['message']
    if room in rooms:
        rooms[room].append({'username': username, 'message': message})
    else:
        rooms[room] = [{'username': username, 'message': message}]
    emit('message', {'username': username, 'message': message}, room=room, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
