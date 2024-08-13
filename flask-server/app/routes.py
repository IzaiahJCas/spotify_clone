from flask import Blueprint, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
import os
import yt_dlp
from . import ChatTest
from . import db
from .models import SongBook

main = Blueprint('main', __name__, static_folder="../build", static_url_path="/")
upload_folder = os.path.join('app', 'SongStorage')
upload_folder_extended = os.path.join('SongStorage')
video_folder = os.path.join('app', 'VideoStorage')
video_folder_extended = os.path.join('VideoStorage')
print(upload_folder)

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
        print(f"song_names: {song_names}")
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
    
    print("audio", audio_files)
    print("video", video_files)
    for song in titles:
        audio_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(upload_folder, f"{secure_filename(song)}.mp4"),
            'quiet': True,
        }
        
        video_opts = {
            'format': 'bestvideo',
            'outtmpl': os.path.join(video_folder, f"{secure_filename(song)}_video.mp4"),
            'quiet': True,
        }

        try:
            with yt_dlp.YoutubeDL(audio_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{song}", download=True)
                audio_file = ydl.prepare_filename(info)
                audio_files.append(audio_file)
                song_names.append(song)
                print(f"Downloaded: {audio_file}")
        
            with yt_dlp.YoutubeDL(video_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{song}", download=True)
                video_file = ydl.prepare_filename(info)
                video_files.append(video_file)
                song_names.append(song)
                print(f"Downloaded: {video_file}")
                
        except Exception as e:
            print(f"Failed to download {song}: {e}")
            continue
    
    return audio_files, song_names, video_files

##Helper method to put file onto database
def upload_file_to_db(file_path, song_name, video_path):
    file_name = os.path.basename(file_path)
    video_name = os.path.basename(video_path)
    song = SongBook(song_name=song_name, file_name=file_name, file_path=file_path, video_path = video_path, video_name = video_name)
    db.session.add(song)
    db.session.commit()

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
    file_path = os.path.join(upload_folder, filename)
    file_path_send_file = os.path.join(upload_folder_extended, filename)

    # Check if the file exists and serve it
    if os.path.isfile(file_path):
        return send_file(file_path_send_file, as_attachment=False)
    else:
        # If the file does not exist, return a 404 error
        print("audio does not exist!")
        return jsonify({'error': 'File not found'}), 404
    
@main.route('/api/video/<path:videoname>', methods = ['GET'])
def get_video(videoname):
    video_path = os.path.join(video_folder, videoname)
    video_path_send_file = os.path.join(video_folder_extended, videoname)
    print(video_path)
    print(video_folder_extended)
    
    if os.path.isfile(video_path):
        print(video_path)
        print(video_folder_extended)
        print("this video exists")
        return send_file(video_path_send_file, as_attachment=False)
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



