import os
from flask import Flask, request, redirect, url_for, render_template_string
from urllib.parse import quote  # Import the quote function

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template_string('''
    <!doctype html>
    <title>Upload Video</title>
    <h1>Upload a Video</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    ''')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        bbcode = f'[video]{url_for("uploaded_file", filename=quote(filename), _external=True)}[/video]'
        return render_template_string('''
        <!doctype html>
        <title>Video Uploaded</title>
        <h1>Video Uploaded</h1>
        <p>BBCode:</p>
        <textarea readonly style="width: 100%; height: 100px;">{{ bbcode }}</textarea>
        <br>
        <a href="/">Upload Another Video</a>
        ''', bbcode=bbcode)
    return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename))

if __name__ == '__main__':
    app.run(debug=True)
