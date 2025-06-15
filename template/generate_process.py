import os
import subprocess
from text_to_audio import text_to_speech_file

def text_to_audio(folder):
    with open(f"user_uploads/{folder}/desc.txt") as f:
        text = f.read()
    print(text, folder)
    text_to_speech_file(text, folder)

def create_reel(folder):
    try:
        input_txt = f"user_uploads/{folder}/input.txt"
        audio_file = f"user_uploads/{folder}/audio.mp3"
        output_file = f"static/reels/{folder}.mp4"
        thumbnail_path = f"static/reels/{folder}.jpg"

        input_files = os.listdir(f"user_uploads/{folder}")
        has_video = any(f.lower().endswith(('.mp4', '.mov', '.avi')) for f in input_files 
                        if f not in ['desc.txt', 'input.txt', 'audio.mp3'])

        if not has_video:
            first_media = next((f for f in input_files 
                                if f not in ['desc.txt', 'input.txt', 'audio.mp3']), None)
            if first_media:
                subprocess.run([
                    'ffmpeg',
                    '-i', f"user_uploads/{folder}/{first_media}",
                    '-ss', '00:00:00',
                    '-vframes', '1',
                    '-q:v', '2',
                    '-vf', 'scale=320:-1',
                    thumbnail_path
                ], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        command = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', input_txt,
            '-i', audio_file,
            '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-shortest',
            '-r', '30',
            '-pix_fmt', 'yuv420p',
            output_file
        ]
        subprocess.run(command, check=True)

    except Exception as e:
        print(f"Error creating reel: {str(e)}")
        raise

# ✅ New function to be called from main.py
def process_folder(folder):
    text_to_audio(folder)
    create_reel(folder)
    with open("done.txt", "a") as f:
        f.write(folder + "\n")
