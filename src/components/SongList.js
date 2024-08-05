import React, { useState, useEffect, useRef } from "react";
import { Container, Row, Col } from "react-bootstrap";
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
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef(null);

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
    resetAudioList();
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
    <Container>
      <h1>Song List</h1>
      <button onClick={fetchAudioList} variant="danger">
        Reset Songs
      </button>
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      <Row>
        <Col className="d-flex flex-column">
          <ul>
            {audioList.map((item, index) => (
              <li
                key={index}
                onClick={() => switchSongs(item)}
                style={{ cursor: "pointer" }}
              >
                {item.song_name}
                <div>
                  <button onClick={handleDelete}> delete </button>
                </div>
              </li>
            ))}
          </ul>
        </Col>
      </Row>
    </Container>
  );
}

export default SongList;
