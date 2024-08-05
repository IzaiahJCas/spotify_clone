import React, { useState, useEffect, useRef } from "react";
import { Container, div } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import PlayButton from "../PlayButton";
import "./SongList.css";

function SongList({
  currentSong,
  setCurrentSong,
  songPlaying,
  setSongPlaying,
  songTitle,
  setSongTitle,
}) {
  const [audioList, setAudioList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeIndex, setActiveIndex] = useState(null);

  async function fetchAudioList() {
    setLoading(true);
    try {
      const response = await fetch("/song_request");
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

  async function resetAudioList() {
    try {
      const response = await fetch("/song_request");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      await fetchAudioList();
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  }

  useEffect(() => {
    fetchAudioList();
  }, []);

  function switchSongs(item) {
    if (currentSong === null && songPlaying === null) {
      setCurrentSong(`/${item.file_name}`);
      setSongPlaying(null);
      setSongTitle(item.song_name);
    } else if (currentSong !== null && songPlaying === null) {
      setCurrentSong(null);
      setSongPlaying(`/${item.file_name}`);
      setSongTitle(item.song_name);
    } else if (currentSong === null && songPlaying !== null) {
      setCurrentSong(`/${item.file_name}`);
      setSongPlaying(null);
      setSongTitle(item.song_name);
    } else {
      console.log("bad things");
    }
  }

  const handleClick = (item, index) => {
    setActiveIndex(index);
    switchSongs(item);
  };

  const handleDelete = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("/delete_songs", {
        method: "POST",
        headers: {
          "content-type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const result = await response.json();

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
                  <button onClick={handleDelete} className="border-black">
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
