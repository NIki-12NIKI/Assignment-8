from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import eventlet
import logging

# Initialize the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize SocketIO with the Flask app
socketio = SocketIO(app, async_mode='eventlet', logger=True, engineio_logger=True)

app.logger.setLevel(logging.DEBUG)
app.logger.setLevel(logging.INFO)
# Notification event to broadcast messages
@socketio.on('send_notification')
def handle_notification(data):
    notification = data.get('notification', 'New update available!')
    
    # Print the message to the terminal
    print(f"Notification received: {notification}")
    
    # Log it using Flask's logger
    app.logger.info(f"Notification received and broadcast: {notification}")
    
    # Broadcast the notification to all clients
    emit('receive_notification', {'notification': notification}, broadcast=True)

@socketio.on('connect')
def on_connect():
    print('Client connected')
    app.logger.info('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')
    app.logger.info('Client disconnected')

@app.route('/')
def index():
    print("Home page accessed!")  # This should appear in the terminal
    return render_template('index2.html')


@app.route('/send_update', methods=['POST'])
def send_update():
    notification = request.form.get('notification')
    # Manually trigger the notification event
    socketio.emit('receive_notification', {'notification': notification}, broadcast=True)
    return jsonify({"status": "Notification sent"}), 200

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5005, debug=True)
