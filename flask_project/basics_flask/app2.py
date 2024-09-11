from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data
users = {
    "alice": {"age": 30, "city": "New York"},
    "bob": {"age": 25, "city": "San Francisco"},
    "charlie": {"age": 35, "city": "Los Angeles"}
}

@app.route('/profile/<username>')
@app.route('/profile/<username>/<int:age>')
@app.route('/profile/<username>/<int:age>/<city>')
def profile(username, age=None, city=None):
    user_data = users.get(username.lower(), {})
    
    if not user_data:
        return f"User {username} not found.", 404
    
    response = f"Profile of {username}:\n"
    
    if age is not None:
        response += f"Age: {age}\n"
    else:
        response += f"Age: {user_data.get('age', 'Not provided')}\n"
    
    if city is not None:
        response += f"City: {city}\n"
    else:
        response += f"City: {user_data.get('city', 'Not provided')}\n"
    
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)
