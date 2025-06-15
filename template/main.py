from flask import Flask, flash, jsonify, render_template, request, redirect, url_for
import uuid
import os
import shutil
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from generate_process import process_folder  # ✅ Imported new function

load_dotenv()

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
        
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], rect_id), exist_ok=True)
        
        with open(os.path.join(app.config['UPLOAD_FOLDER'], rect_id, "desc.txt"), "w") as f:
            f.write(desc)
        
        media_files = []
        for file in request.files.getlist('media'):
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], rect_id, filename)
                file.save(file_path)
                media_files.append(filename)
        
        if not media_files:
            flash('No valid files uploaded')
            return redirect(request.url)
        
        with open(os.path.join(app.config['UPLOAD_FOLDER'], rect_id, "input.txt"), "w") as f:
            for filename in media_files:
                ext = os.path.splitext(filename)[1].lower()
                if ext in ['.mp4', '.mov', '.avi']:
                    f.write(f"file '{filename}'\n")
                else:
                    f.write(f"file '{filename}'\nduration 3\n")

        # ✅ Generate reel immediately
        process_folder(rect_id)

        flash("Upload successful. Audio & reel generation are currently paused. Demo reels are in the gallery.", "info")
        return render_template("create.html", my_id=my_id)
    
    return render_template("create.html", my_id=my_id)

@app.route('/delete_reel/<reel_name>', methods=['DELETE'])
def delete_reel(reel_name):
    try:
        if not reel_name.replace('-', '').isalnum():
            return jsonify({'success': False, 'error': 'Invalid reel name'}), 400
        
        video_path = os.path.join('static', 'reels', f'{reel_name}.mp4')
        thumb_path = os.path.join('static', 'reels', f'{reel_name}.jpg')
        
        for path in [video_path, thumb_path]:
            if os.path.exists(path):
                os.remove(path)
        
        upload_folder = os.path.join('user_uploads', reel_name)
        if os.path.exists(upload_folder):
            shutil.rmtree(upload_folder)
        
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
    
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
    
    
