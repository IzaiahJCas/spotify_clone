from flask import Flask, render_template, request, redirect, url_for, jsonify
from pytube import YouTube
from pytube import Search
from flask_cors import CORS
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import argparse
import ChatTest
import psycopg2
import time
import yt_dlp


#Create a Flask Instance
app = Flask(__name__)
CORS(app)

load_dotenv()

##SQLAlchemy
class Base(DeclarativeBase):
  pass

POSTGRES_URL = os.getenv('POSTGRES_URL')

app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

app.config['UPLOAD_FOLDER'] = r"C:\Users\donut\spotify_clone\flask-server\SongStorage"
upload_folder = app.config['UPLOAD_FOLDER']

class SongBook(db.Model):
    __tablename__ = 'song_catalog'
    id: Mapped[int] = mapped_column(primary_key=True)
    song_name: Mapped[str] = mapped_column(unique=True)
    file_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    file_path: Mapped[str] = mapped_column(unique=True, nullable=False)
    
with app.app_context():
    db.create_all()

##Youtube app Search Script
urls = []
videoUrl = ''
app = Flask(__name__)

##Grab form data from front-end
@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.get_json()
    amount = data.get('amount')
    artist = data.get('artist')
    name = data.get('name')
    
    downloaded_files, song_names = YoutubeAudioDownload(amount, artist, name)    

    return jsonify({'downloaded_files': downloaded_files, 'song_names': song_names})

def YoutubeAudioDownload(amount, artist, name):
    user_input = f"Can you give me the titles of {amount} more songs that sound like {artist}'s {name}, don't explain anything just give me the titles please, Including the song I gave you."
    response = ChatTest.talk_to_bot(user_input)
    titles = ChatTest.extract_titles(response)
    print(user_input)
    
    
    downloaded_files = []
    song_names = []
    for song in titles:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(upload_folder, f"{secure_filename(song)}.%(ext)s"),
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

# ##Used to upload file from path
# def upload_file_from_path(file, file_name, song_name):
#     if file:
#         file_path = os.path.join(upload_folder, file_name)
#         with open(file_path, 'wb') as f:
#             f.write(file.read())
            
#         song = SongBook(song_name=song_name, file_name=file_name, file_path=file_path)
#         db.session.add(song)
#         db.session.commit()
        
#         return jsonify({'message': 'File successfully uploaded'}), 201
    
# ##Take files and perform a POST request
# @app.route("/upload", methods = ['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part in the request'}), 400
    
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No file selected for uploading'}), 400

#     if file:
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(upload_folder, filename)
#         file.save(file_path)
        
#         # Add file info to the database
#         song = SongBook(song_name=request.form['song_name'], file_name=filename, file_path=file_path)
#         db.session.add(song)
#         db.session.commit()

#         return jsonify({'message': 'File successfully uploaded'}), 201

# ##Used to retrieve uploaded files
# @app.route('/files', methods=['GET'])
# def get_files():
#     songs = SongBook.query.all()
#     song_list = []
#     for song in songs:
#         song_data = {
#             'id': song.id,
#             'song_name': song.song_name,
#             'file_name': song.file_name,
#             'file_path': song.file_path
#         }
#         song_list.append(song_data)
    
#     return jsonify(song_list), 200

if __name__ == "__main__":
        app.run(debug=True)
   
        
      
        
    