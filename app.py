from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import markdown.extensions.fenced_code
from helper import Helper
from datetime import date
from queue_order.queue import Queue
import os

app = Flask('__name__')
UPLOAD_FOLDER = 'upload_folder'
ALLOWED_EXTENSIONS = {'docx'}

@app.route('/')
def index():
    readme_file = open("README.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )
    return md_template_string

@app.route('/next_day_queue', methods = ['GET'])
def uploadFile():
    return render_template('upload.html')

@app.route('/next_day_queue', methods = ['POST'])
def nextDayQueue():
    upload_file = request.files['file']
    baseline = request.form['baseline']
    print(baseline)
    if Helper.allowedFile(upload_file.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(upload_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], Helper.getFileName(Helper.getFileExtension(filename)))
        upload_file.save(filepath)
        queue = Queue(baseline, filepath)
        data = queue.getNextDayQueue()
        
        return render_template('upload.html', data=data, )
    else:
        return 'invalid extension'

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.run(debug=True)