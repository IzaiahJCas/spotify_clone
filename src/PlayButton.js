import { Button, Col } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { FaPlay } from "react-icons/fa";
import React, { useState, useEffect } from "react";

function PlayButton() {
  const [audioList, setAudioList] = useState([]);
  const [selectedAudio, setSelectedAudio] = useState("");

  // Fetch the list of audio files from the backend
  async function fetchAudioList() {
    try {
      const response = await fetch("/audio");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      setAudioList(data);
    } catch (error) {
      console.error("Failed to fetch audio list:", error);
    }
  }

  useEffect(() => {
    fetchAudioList();
  }, []);

  return (
    <div className="container">
      <h1>Audio Player</h1>
    </div>
  );
}

export default PlayButton;
