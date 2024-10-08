import { Button, Col } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { IoPlayCircle } from "react-icons/io5";
import { RxSpeakerLoud } from "react-icons/rx";
import React, { useState, useEffect } from "react";
import "./PlayButton.css";

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${minutes}:${secs < 10 ? "0" : ""}${secs}`;
}

function PlayButton({
  playAndPause,
  currentSong,
  songPlaying,
  audioRef,
  volume,
  setVolume,
  videoRef,
  currentVideo,
  videoPlaying,
}) {
  const [currentTime, setCurrentTime] = useState(0);
  const [songDuration, setSongDuration] = useState(0);

  const songTime = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
      setSongDuration(audioRef.current.duration);
    }
  };

  useEffect(() => {
    const interval = setInterval(songTime, 1000);
    return () => clearInterval(interval);
  }, []);

  const volumeBarChange = (event) => {
    if (audioRef.current) {
      setVolume(event.target.value);
      audioRef.current.volume = volume;
    }
    const value = event.target.value * 100; // Convert to percentage
    event.target.style.setProperty("--value", `${value}%`);
  };

  return (
    <div className="container">
      <div className="row background-color">
        <div className="col d-flex justify-content-end">
          <button onClick={playAndPause} className="play-button">
            <IoPlayCircle />
          </button>
          {(currentSong || songPlaying) && (
            <div>
              <audio ref={audioRef} key={currentSong || songPlaying}>
                <source src={currentSong || songPlaying} type="audio/mp4" />
                Your browser does not support the audio element.
              </audio>
            </div>
          )}
        </div>
        <div className="col d-flex justify-content-end align-items-center gap volume-component">
          <RxSpeakerLoud />
          <input
            type="range"
            max={1}
            min={0}
            step={0.02}
            value={volume}
            onChange={volumeBarChange}
            className="volume-bar"
          />
        </div>
        <div className="row">
          <div className="col-auto text-white">
            <p>{formatTime(currentTime)}</p>
          </div>
          <div className="col">
            <input
              type="range"
              max={songDuration}
              min={0}
              step={0.02}
              value={currentTime}
              className="song-bar"
            />
          </div>
          <div className="col-auto text-white">
            <p>{formatTime(songDuration)}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PlayButton;
