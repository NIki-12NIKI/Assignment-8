from flask import Flask, render_template, request

app = Flask(__name__)

# Route for displaying the form
@app.route('/')
def form():
    return render_template('form.html')

# Route for handling form submission and displaying the result
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        return render_template('result.html', name=name, email=email)

if __name__ == '__main__':
    app.run(host="0.0.0.0" , port = 5003)
