import os
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Define the uploads directory
UPLOAD_FOLDER = 'uploads'  
# Set allowed extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def main():
    return render_template("submit.html")

@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400
        
        f = request.files['file']

        if f.filename == '':
            return "No selected file", 400
        
        if f and allowed_file(f.filename):
            # Create the uploads directory if it doesn't exist
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            # Save the file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            f.save(file_path)  # save to uploads directory
            
            return render_template("ack.html", name=f.filename)
        else:
            return "File type not allowed", 400

if __name__ == '__main__':
    app.run(debug=True)
