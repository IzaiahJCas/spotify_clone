from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import Mapped, mapped_column
import os
import ChatTest
import yt_dlp

#Create a Flask Instance
app = Flask(__name__)
CORS(app)

##Load env variables
load_dotenv()

##SQLAlchemy configs
POSTGRES_URL = os.getenv('POSTGRES_URL')
app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy()
migrate = Migrate(app, db)

#Define the SongBook model
class SongBook(db.Model):
    __tablename__ = 'test_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    song_name: Mapped[str] = mapped_column(unique=True)
    file_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    file_path: Mapped[str] = mapped_column(unique=True, nullable=False)

#upload folder
app.config['UPLOAD_FOLDER'] = r"C:\Users\donut\spotify_clone\flask-server\SongStorage"
upload_folder = app.config['UPLOAD_FOLDER']

@app.route('/')
def index():
    return 'Hello, World!'

##Grab form data from front-end
@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.get_json()
    amount = data.get('amount')
    artist = data.get('artist')
    name = data.get('name')
    
    downloaded_files, song_names = YoutubeAudioDownload(amount, artist, name)  
    for file_path, song_name in zip(downloaded_files, song_names):
        upload_file_to_db(file_path, song_name)  

    return jsonify({'downloaded_files': downloaded_files, 'song_names': song_names})

##Youtube app Search Script
urls = []
videoUrl = ''
def YoutubeAudioDownload(amount, artist, name):
    user_input = f"Can you give me the titles of {amount} more songs that sound like {artist}'s {name}, don't explain anything just give me the titles please, Including the song I gave you."
    response = ChatTest.talk_to_bot(user_input)
    titles = ChatTest.extract_titles(response)
    
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

##Used to put the file into the db
def upload_file_to_db(file_path, song_name):
    file_name = os.path.basename(file_path)
    song = SongBook(song_name=song_name, file_name=file_name, file_path=file_path)
    db.session.add(song)
    db.session.commit()

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
   
        
      
        
    