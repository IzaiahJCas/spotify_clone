import argparse
import sys 
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pytube import YouTube
from pytube import Search
from flask_cors import CORS


AUDIO_DOWNLOAD_DIR = r"C:\Users\donut\Music"
urls = []
videoUrl = ''

app = Flask(__name__)
CORS(app)

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
 app.run(debug=True)