from flask import Flask, render_template, request, redirect, url_for, jsonify
from pytube import YouTube
from pytube import Search
from flask_cors import CORS
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import os
import argparse
import ChatTest
import psycopg2
import time


#Create a Flask Instance
app = Flask(__name__)
CORS(app)

load_dotenv()

##SQLAlchemy
class Base(DeclarativeBase):
  pass


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://default:ygqNv2ALmr5P@ep-green-shadow-a4h7g7o9-pooler.us-east-1.aws.neon.tech/verceldb?sslmode=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

class SongBook(db.Model):
    __tablename__ = 'song_book'
    id: Mapped[int] = mapped_column(primary_key=True)
    song_name: Mapped[str] = mapped_column(unique=True)
    
with app.app_context():
    db.create_all()

##Youtube app Search Script
AUDIO_DOWNLOAD_DIR = r"C:\Users\donut\Music"
urls = []
videoUrl = ''
currentVideo = 0
app = Flask(__name__)

@app.route("/YoutubeAudioDownload")
def YoutubeAudioDownload():
    ap = argparse.ArgumentParser()
    ap.add_argument("Artist", help="Artist of the song")
    ap.add_argument("Song", help="Title of the song")
    ap.add_argument("Amount", help="Amount of songs wanted")
    
    args = ap.parse_args()
    amount = args.Amount
    artist = args.Artist
    song = args.Song
    
    user_input = f"Can you give me the titles of {amount} more songs that sound like {artist}'s {song}, don't explain anything just give me the titles please, Including the song I gave you."
    response = ChatTest.talk_to_bot(user_input)
    titles = ChatTest.extract_titles(response)
    print(titles)
    
    for i, song in enumerate(titles): 
        print(song)
        s = Search(song)
        for v in s.results:
            urls.append(v.watch_url)
            break
        videoUrl = urls[i]
        video = YouTube(videoUrl)
        audio_stream = video.streams.filter(only_audio=True, file_extension="mp4", adaptive=True).first()
    
        try:
            audio_stream.download(AUDIO_DOWNLOAD_DIR)
            print("Download Success")
        except Exception as e:
            print(f"Failed to download: {e}")
        

if __name__ == "__main__":
        
        app.run(debug=True)
   
        
      
        
    