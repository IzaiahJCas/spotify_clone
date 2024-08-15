import React, { useState, useEffect, useRef } from "react";
import { Container, div } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import PlayButton from "../PlayButton";
import "./SongList.css";
import VideoPlayer from "./VideoPlayer";

function SongList({
  currentSong,
  setCurrentSong,
  songPlaying,
  setSongPlaying,
  songTitle,
  setSongTitle,
  setCurrentVideo,
  currentVideo,
  setVideoPlaying,
  videoPlaying,
  refresh,
  setRefresh,
}) {
  const [audioList, setAudioList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeIndex, setActiveIndex] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);

  async function fetchAudioList() {
    setLoading(true);
    try {
      const response = await fetch("/api/song_request");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const result = await response.json();
      setAudioList(result);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (refresh) {
      fetchAudioList();
      setRefresh(false);
    }
  }, [refresh]);

  async function fetchFirebaseAudio(filename) {
    setLoading(true); // Set loading to true at the start
    try {
      const response = await fetch(`/api/audio/${filename}`);
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const result = await response.json();
      return result.audio_url; // Return the audio URL
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false); // Set loading to false in the finally block
    }
  }

  async function fetchFirebaseVideo(filename) {
    setLoading(true); // Set loading to true at the start
    try {
      const response = await fetch(`/api/video/${filename}`);
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const result = await response.json();
      return result.video_url; // Return the video URL
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false); // Set loading to false in the finally block
    }
  }

  async function switchSongs(item) {
    setLoading(true); // Optionally show a loading state

    try {
      const audioUrl = await fetchFirebaseAudio(item.file_name);
      const videoUrl = await fetchFirebaseVideo(item.video_name);

      if (currentSong === null && songPlaying === null) {
        setCurrentSong(audioUrl);
        setSongPlaying(null);
        setSongTitle(item.song_name);
        setCurrentVideo(videoUrl);
        setVideoPlaying(null);
      } else if (currentSong !== null && songPlaying === null) {
        setCurrentSong(null);
        setSongPlaying(audioUrl);
        setSongTitle(item.song_name);
        setCurrentVideo(null);
        setVideoPlaying(videoUrl);
      } else if (currentSong === null && songPlaying !== null) {
        setCurrentSong(audioUrl);
        setSongPlaying(null);
        setSongTitle(item.song_name);
        setCurrentVideo(null);
        setVideoPlaying(videoUrl);
      } else {
        console.log("bad things");
      }
    } catch (error) {
      console.error("Error in switchSongs:", error.message);
    } finally {
      setLoading(false); // Hide loading state
    }
  }

  const handleClick = (item, index) => {
    setActiveIndex(index);
    switchSongs(item);
  };

  const handleDelete = async (e, item) => {
    e.stopPropagation();
    e.preventDefault();

    try {
      const response = await fetch("/api/delete_songs", {
        method: "POST",
        headers: {
          "content-type": "application/json",
        },
        body: JSON.stringify({ filename: item.file_name }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const result = await response.json();
      setRefresh(true);
      console.log(result);
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };

  return (
    <div class="h-full overflow-auto scrollbar-hide text-center">
      <h1 className="text-blue-400 mt-2 text-shadow-glowing">Song List</h1>
      <button
        onClick={fetchAudioList}
        variant="danger"
        className="shadow-md shadow-blue-400/70 text-blue-400 rounded-md border-2 border-blue-400 p-2 mt-4 mb-2 hover:bg-white/10 transition-colors duration-300"
      >
        Reset Songs
      </button>
      <div>
        <div>
          <ul className="text-blue-400 text-center text-shadow">
            {audioList.map((item, index) => (
              <li
                key={index}
                onClick={() => handleClick(item, index)}
                style={{ cursor: "pointer" }}
                class={`flex flex-row justify-between rounded-lg w-full p-4 song-item ${
                  activeIndex === index
                    ? "bg-transparent border-blue-400 border-y-2 shadow-custom-shadow"
                    : "hover:bg-white/10"
                }`}
              >
                {item.song_name}
                <div>
                  <button
                    onClick={(e) => handleDelete(e, item)}
                    className="border-black"
                  >
                    X
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default SongList;
