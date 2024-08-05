This project aims to use Google's Gemini AI API in order to fetch song titles to compile playlists using the AI's discretion on what songs sound like one another.

The songs are downloaded using yt-dlp, using a python script to download both the video and the audio.

The UI allows the user to type in the amount of songs they want in their playlist, the artist and artist's song which the playlist should be built around. This information is posted using JSON to the python backend and fed through a prompt to Gemini AI.

Afterwards the files are downloaded to a file system, and the paths are saved within a SQL table for retrieval through the front-end when requested.
