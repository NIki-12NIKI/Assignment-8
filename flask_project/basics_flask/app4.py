from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)

# Secret key is needed to secure the session
app.secret_key = 'your_secret_key'

# Uncomment below if you are using Flask-Session for server-side session storage
# from flask_session import Session
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

@app.route('/')
def home():
    # Check if the user is already logged in
    if 'name' in session:
        return redirect(url_for('dashboard'))
    return render_template('form1.html')

@app.route('/login', methods=['POST'])
def login():
    # Get the user's name from the form
    name = request.form['name']
    # Store the name in session
    session['name'] = name
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # If the user is not logged in, redirect them to the login form
    if 'name' not in session:
        return redirect(url_for('home'))
    # Render the dashboard template with the user-specific data
    return render_template('dashboard.html', name=session['name'])

@app.route('/logout')
def logout():
    # Remove the user's name from the session
    session.pop('name', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host="0.0.0.0" , port = 5004)
