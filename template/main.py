from flask import Flask, flash, jsonify, render_template, request, redirect, url_for
import uuid
import os
import shutil
from werkzeug.utils import secure_filename

from dotenv import load_dotenv
load_dotenv()

import os
app = Flask(__name__)



UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'mov', 'avi'}

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_dev_key')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    my_id = str(uuid.uuid1())
    if request.method == "POST":
        rect_id = request.form.get("uuid")
        desc = request.form.get("text")
        
        if not rect_id or not desc:
            flash('Missing required fields')
            return redirect(request.url)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], rect_id), exist_ok=True)
        
        # Save description
        with open(os.path.join(app.config['UPLOAD_FOLDER'], rect_id, "desc.txt"), "w") as f:
            f.write(desc)
        
        # Process uploaded files - using getlist() for multiple files
        media_files = []
        for file in request.files.getlist('media'):  # Changed to getlist
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], rect_id, filename)
                file.save(file_path)
                media_files.append(filename)
        
        if not media_files:
            flash('No valid files uploaded')
            return redirect(request.url)
        
        # Generate input.txt based on file types
        with open(os.path.join(app.config['UPLOAD_FOLDER'], rect_id, "input.txt"), "w") as f:
            for filename in media_files:
                ext = os.path.splitext(filename)[1].lower()
                if ext in ['.mp4', '.mov', '.avi']:  # Video files
                    f.write(f"file '{filename}'\n")
                else:  # Image files
                    f.write(f"file '{filename}'\nduration 3\n")  # Default 3 sec per image
        
        flash("Reel is created in gallery", "success")
        return render_template("create.html", my_id=my_id) 
    
    return render_template("create.html", my_id=my_id)


@app.route('/delete_reel/<reel_name>', methods=['DELETE'])
def delete_reel(reel_name):
    try:
        # Security check
        if not reel_name.replace('-', '').isalnum():
            return jsonify({'success': False, 'error': 'Invalid reel name'}), 400
        
        # 1. Delete from static/reels/
        video_path = os.path.join('static', 'reels', f'{reel_name}.mp4')
        thumb_path = os.path.join('static', 'reels', f'{reel_name}.jpg')
        
        for path in [video_path, thumb_path]:
            if os.path.exists(path):
                os.remove(path)
        
        # 2. Delete from user_uploads/
        upload_folder = os.path.join('user_uploads', reel_name)
        if os.path.exists(upload_folder):
            shutil.rmtree(upload_folder)
        
        # 3. Remove from done.txt
        if os.path.exists('done.txt'):
            with open('done.txt', 'r') as f:
                done_folders = [line.strip() for line in f.readlines() if line.strip()]
            
            with open('done.txt', 'w') as f:
                for folder in done_folders:
                    if folder != reel_name:
                        f.write(f"{folder}\n")
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route("/gallery")
def gallery():
    if not os.path.exists('static/reels'):
        os.makedirs('static/reels')
    reels = [f for f in os.listdir("static/reels") if f.endswith('.mp4')]
    return render_template("gallery.html", reels=reels)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists('static/reels'):
        os.makedirs('static/reels')
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT automatically
    app.run(host="0.0.0.0", port=port)