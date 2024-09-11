from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Configuring the folder for file uploads
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']

        # If no file is selected
        if file.filename == '':
            return 'No selected file'
        
        if file:
            # Save the file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            return redirect(url_for('index'))
    
    # Get list of uploaded files to display
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', uploaded_files=uploaded_files)

if __name__ == '__main__':
    app.run(host="0.0.0.0" , port = 5005)
