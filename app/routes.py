# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from app.services.s3_service import upload_file_to_s3
from app.services.chatgpt_service import analyze_with_chatgpt
from werkzeug.utils import secure_filename
import os

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Analyze with ChatGPT first (using the file directly)
        analysis = analyze_with_chatgpt(file)
        
        # Then upload to S3 (need to reset file pointer first)
        file.seek(0)
        s3_path = upload_file_to_s3(file, filename)
        
        return render_template('result.html', analysis=analysis)
    
    return 'Invalid file type', 400