from flask import Flask, render_template, request, redirect, url_for, jsonify
from pytube import YouTube
from pytube import Search
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime



#Create a Flask Instance
app = Flask(__name__)
CORS(app)

#Add Database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://SearchScript.db'
#Key
app.config['SECRET_KEY'] = "my key"
#DB intialization
db.init_app(app)

#Create Model
class Songs(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False, unique = True)
    ## genre = db.Column(db.String(50), nullable = False)
    ## song_length = db.Column(db.Integer, nullable = False)
    ## artist = db.Column(db.String(50), nullable = False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    
    #Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

#Variables for the script
AUDIO_DOWNLOAD_DIR = db
urls = []
videoUrl = ''

#Main Script Code
@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/YoutubeAudioDownload", methods =['POST', 'GET'])
def YoutubeAudioDownload():
    data = request.get_json('SearchBar.js')
    song_name = data.get('songName')
    s = Search(song_name)
    for v in s.results:
        urls.append(v.watch_url)
        break
    videoUrl = urls[0]
    video = YouTube(videoUrl)
    audio_stream = video.streams.filter(only_audio=True).first()
    
    try:
        audio_stream.download(AUDIO_DOWNLOAD_DIR)
    except Exception as e:
        print(f"Failed to download: {e}")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)