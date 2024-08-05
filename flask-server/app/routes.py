from flask import Blueprint, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
import os
import yt_dlp
from . import ChatTest
from . import db
from .models import SongBook

main = Blueprint('main', __name__)
upload_folder = os.path.join('app', 'SongStorage')
upload_folder_extended = os.path.join('SongStorage')
print(upload_folder)
## Puts the file onto the database
@main.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.get_json()
    amount = data.get('amount')
    artist = data.get('artist')
    name = data.get('name')
    
    downloaded_files, song_names = YoutubeAudioDownload(amount, artist, name)  
    for file_path, song_name in zip(downloaded_files, song_names):
        upload_file_to_db(file_path, song_name)  

    return jsonify({'downloaded_files': downloaded_files, 'song_names': song_names})

## Youtube download script
def YoutubeAudioDownload(amount, artist, name):
    user_input = f"Can you give me the titles of {amount} more songs that sound like {artist}'s {name}, don't explain anything just give me the titles please, Including the song I gave you."
    response = ChatTest.talk_to_bot(user_input)
    titles = ChatTest.extract_titles(response)
    
    downloaded_files = []
    song_names = []
    for song in titles:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(upload_folder, f"{secure_filename(song)}.mp4"),
            'quiet': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{song}", download=True)
                downloaded_file = ydl.prepare_filename(info)
                downloaded_files.append(downloaded_file)
                song_names.append(song)
                print(f"Downloaded: {downloaded_file}")
                
        except Exception as e:
            print(f"Failed to download {song}: {e}")
            continue
    
    return downloaded_files, song_names

##Helper method to put file onto database
def upload_file_to_db(file_path, song_name):
    file_name = os.path.basename(file_path)
    song = SongBook(song_name=song_name, file_name=file_name, file_path=file_path)
    db.session.add(song)
    db.session.commit()

##Requests the song name and filepath from the database
@main.route('/song_request', methods=['GET'])
def get_song_name():
    try:
        songs = db.session.query(SongBook.file_path, SongBook.song_name, SongBook.file_name).all()
        song_list = []
        for song in songs:
            song_data = {
            'song_name': song.song_name,
            'file_path': song.file_path,
            'file_name': song.file_name
             }
            song_list.append(song_data)
        return jsonify(song_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



##Plays the audio from the file
@main.route('/<path:filename>', methods=['GET'])
def get_audio(filename):
   # Join the upload folder with the filename to get the full file path
    file_path = os.path.join(upload_folder, filename)
    file_path_send_file = os.path.join(upload_folder_extended, filename)

    # Check if the file exists and serve it
    if os.path.isfile(file_path):
        return send_file(file_path_send_file, as_attachment=False)
    else:
        # If the file does not exist, return a 404 error
        print("File does not exist!")
        return jsonify({'error': 'File not found'}), 404
    
@main.route('/delete_songs', methods=['POST'])
def delete_songs(filename):
    song_to_delete = db.session.query(SongBook).filter(SongBook.file_name == filename).first()
    try:
        if song_to_delete:
            db.session.delete(song_to_delete)
            db.session.commit()
            return jsonify({'message': 'All songs deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



