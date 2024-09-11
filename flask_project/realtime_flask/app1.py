from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO, emit, join_room, leave_room
import eventlet

# Initialize the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////config/workspace/flask_project/realtime_flask/instance/chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-SocketIO and SQLAlchemy
db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode='eventlet')

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Chat message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    room = db.Column(db.String(80), nullable=False)


# Load user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    return render_template('index1.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Failed. Check username and password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/chat/<room>')
@login_required
def chat(room):
    messages = Message.query.filter_by(room=room).all()
    return render_template('chat.html', room=room, messages=messages)

# SocketIO event handlers
@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('notification', f"{current_user.username} has entered the room.", to=room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    emit('notification', f"{current_user.username} has left the room.", to=room)

@socketio.on('send_message')
def handle_message(data):
    room = data['room']
    message = data['message']
    # Save message to the database
    new_message = Message(username=current_user.username, message=message, room=room)
    db.session.add(new_message)
    db.session.commit()
    emit('receive_message', {'username': current_user.username, 'message': message}, to=room)

@socketio.on('typing')
def handle_typing(data):
    room = data['room']
    emit('typing', f"{current_user.username} is typing...", to=room, broadcast=False)

if __name__ == '__main__':
    # Create all tables within the app context
    with app.app_context():
        db.create_all()  # Ensure this is executed within the app context
    # Run the app with SocketIO
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

