import React, { useState, useEffect } from "react";
import { Container, Row, Col } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

function SongList() {
  const [audioList, setAudioList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentSong, setCurrentSong] = useState(null);

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

  useEffect(() => {
    fetchAudioList();
  }, []);

  function handleSongClick(item) {
    console.log("Selected song:", item);
    setCurrentSong(`/${item.file_name}`);
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
      <button onClick={handleDelete} variant="danger">
        Reset Songs
      </button>
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      <Row>
        <Col>
          <ul>
            {audioList.map((item, index) => (
              <li
                key={index}
                onClick={() => handleSongClick(item)}
                style={{ cursor: "pointer" }}
              >
                {item.song_name}
              </li>
            ))}
          </ul>
          {currentSong && (
            <audio controls autoPlay>
              <source src={currentSong} type="audio/mp4" />
              Your browser does not support the audio element.
            </audio>
          )}
        </Col>
      </Row>
    </Container>
  );
}

export default SongList;
