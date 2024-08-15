from flask import Blueprint, request, jsonify, send_from_directory, send_file, request
from werkzeug.utils import secure_filename
import os
import datetime
import requests
import io
import yt_dlp
import tempfile
from . import ChatTest
from . import db
from .models import SongBook
import firebase_admin
from firebase_admin import credentials, storage

main = Blueprint('main', __name__, static_folder="../build", static_url_path="/")
upload_folder = os.path.join('app', 'SongStorage')
upload_folder_extended = os.path.join('SongStorage')
video_folder = os.path.join('app', 'VideoStorage')
video_folder_extended = os.path.join('VideoStorage')
print(upload_folder)

##Firebase storage
service_account_key_path = "./firebase.json"
cred = credentials.Certificate(service_account_key_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'spotify-clone-c211b.appspot.com'  # Replace with your Firebase project storage bucket
})
bucket = storage.bucket()
firebase_audio = 'audio/'
firebase_video = 'video/'

##Access build folder index.html
@main.route('/')
def index():
    return send_from_directory(main.static_folder, 'index.html')
    
## Puts the file onto the database
@main.route('/api/submit_form', methods=['POST'])
def submit_form():
    data = request.get_json()
    amount = data.get('amount')
    artist = data.get('artist')
    name = data.get('name')
    
    
    audio_files, song_names, video_files = YoutubeAudioDownload(amount, artist, name)  
    
    for file_path, song_name, video_path in zip(audio_files, song_names, video_files):
        upload_file_to_db(file_path, song_name, video_path)
  
        print(f"audio_files: {audio_files}")
        print(f"video_files: {video_files}")
    return jsonify({'downloaded_files': audio_files, 'song_names': song_names, 'videos': video_files})

## Youtube download script
def YoutubeAudioDownload(amount, artist, name):
    user_input = f"Can you give me the titles of {amount} more songs that sound like {artist}'s {name}, don't explain anything just give me the titles please, Including the song I gave you."
    response = ChatTest.talk_to_bot(user_input)
    titles = ChatTest.extract_titles(response)
    
    audio_files = []
    song_names = []
    video_files =[]
    
    with tempfile.TemporaryDirectory() as temp_audio_dir, tempfile.TemporaryDirectory() as temp_video_dir:
        for song in titles:
            audio_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(temp_audio_dir, f"{secure_filename(song)}.mp4"),
                'quiet': True,
            }
            
            video_opts = {
                'format': 'bestvideo',
                'outtmpl': os.path.join(temp_video_dir, f"{secure_filename(song)}_video.mp4"),
                'quiet': True,
            }

            try:
                with yt_dlp.YoutubeDL(audio_opts) as ydl:
                    info = ydl.extract_info(f"ytsearch:{song}", download=True)
                    audio_file = ydl.prepare_filename(info)
                    audio_files.append(f"{firebase_audio}{secure_filename(song)}.mp4")
                    song_names.append(song)
                    print(f"Downloaded: {audio_file}")
                    
                    download_and_upload_to_firebase(audio_file, f"{firebase_audio}{secure_filename(song)}.mp4")
            
                with yt_dlp.YoutubeDL(video_opts) as ydl:
                    info = ydl.extract_info(f"ytsearch:{song}", download=True)
                    video_file = ydl.prepare_filename(info)
                    video_files.append(f"{firebase_video}{secure_filename(song)}_video.mp4")
                    song_names.append(song)
                    print(f"Downloaded: {video_file}")
                    
                    download_and_upload_to_firebase(video_file, f"{firebase_video}{secure_filename(song)}_video.mp4")
                    
            except Exception as e:
                print(f"Failed to download {song}: {e}")
                continue
    
    return audio_files, song_names, video_files

def download_and_upload_to_firebase(local_file_path, remote_file_path):
    try:
        # Create a new blob (file) in the bucket
        bucket = storage.bucket()
        blob = bucket.blob(remote_file_path)
        
        # Upload the file content from the local file path to Firebase Storage
        blob.upload_from_filename(local_file_path)
        
        print(f"Upload Successful: {local_file_path} to {remote_file_path}")
    
    except Exception as e:
        print(f"Failed to upload {local_file_path} to Firebase: {e}")    

##Helper method to put file onto database
def upload_file_to_db(file_path, song_name, video_path):
    file_name = os.path.basename(file_path)
    video_name = os.path.basename(video_path)
    song = SongBook(song_name=song_name, file_name=file_name, file_path=file_path, video_path = video_path, video_name = video_name)
    db.session.add(song)
    db.session.commit()

def generate_signed_url(file_path):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(file_path)
        # Generate a signed URL (valid for 1 hour)
        url = blob.generate_signed_url(expiration=datetime.timedelta(hours=1))
        return url
    except Exception as e:
        print(f"Failed to generate URL for {file_path}: {e}")
        return None

##Requests the song name and filepath from the database
@main.route('/api/song_request', methods=['GET'])
def get_song_name():
    try:
        songs = db.session.query(SongBook.file_path, SongBook.song_name, SongBook.file_name, SongBook.video_path, SongBook.video_name).all()
        song_list = []
        for song in songs:
            song_data = {
            'song_name': song.song_name,
            'file_path': song.file_path,
            'file_name': song.file_name,
            'video_path': song.video_path,
            'video_name': song.video_name,
             }
            song_list.append(song_data)
        return jsonify(song_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

##Plays the audio from the file
@main.route('/api/audio/<path:filename>', methods=['GET'])
def get_audio(filename):
   # Join the upload folder with the filename to get the full file path
    file_path = os.path.join(firebase_audio, filename)
    file_content = generate_signed_url(file_path)
    print(file_content)
    # Check if the file exists and serve it
    if file_content:
        return jsonify({'audio_url': file_content})
    else:
        # If the file does not exist, return a 404 error
        print("audio does not exist!")
        return jsonify({'error': 'File not found'}), 404
    
@main.route('/api/video/<path:videoname>', methods = ['GET'])
def get_video(videoname):
    file_path = os.path.join(firebase_video, videoname)
    file_content = generate_signed_url(file_path)
    print(file_content)
    # Check if the file exists and serve it
    if file_content:
        return jsonify({'video_url': file_content})
    else:
        # If the file does not exist, return a 404 error
        print("Video does not exist!")
        return jsonify({'error': 'File not found'}), 404
    
@main.route('/api/delete_songs', methods=['POST'])
def delete_songs():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'Filename is required'}), 400

    song_to_delete = db.session.query(SongBook).filter(SongBook.file_name == filename).first()
    try:
        if song_to_delete:
            db.session.delete(song_to_delete)
            db.session.commit()
            return jsonify({'message': 'All songs deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500