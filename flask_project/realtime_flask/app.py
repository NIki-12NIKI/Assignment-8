from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Serve the chat interface
@app.route('/')
def index():
    return render_template('index.html')

# Handle messages from client
@socketio.on('message')
def handle_message(msg):
    print(f"Message: {msg}")
    send(msg, broadcast=True)

# Handle username connection
@socketio.on('connect')
def handle_connect():
    print("User connected")

# Handle disconnection
@socketio.on('disconnect')
def handle_disconnect():
    print("User disconnected")

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)



