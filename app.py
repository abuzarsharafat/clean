from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import pandas as pd

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/.netlify/functions/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(status='error', message='No file part'), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(status='error', message='No selected file'), 400
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        file.save(file_path)
        return jsonify(status='success', message='File uploaded successfully'), 200
    except Exception as e:
        return jsonify(status='error', message=f'Failed to save file: {str(e)}'), 500

@app.route('/.netlify/functions/clean', methods=['POST'])
def clean_file():
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.listdir(app.config['UPLOAD_FOLDER'])[0])
        df = pd.read_excel(file_path)
        # Example cleaning step
        df.dropna(inplace=True)
        clean_path = os.path.join(app.config['UPLOAD_FOLDER'], 'cleaned_file.xlsx')
        df.to_excel(clean_path, index=False)
        return send_file(clean_path, as_attachment=True)
    except Exception as e:
        return jsonify(status='error', message=f'Failed to clean file: {str(e)}'), 500

if __name__ == '__main__':
    app.run(debug=True)
