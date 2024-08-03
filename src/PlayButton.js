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
  };

  return (
    <div className="container">
      <div className="row ">
        <div className="col d-flex justify-content-end align-items-center">
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
        <div className="col d-flex justify-content-end align-items-center">
          <RxSpeakerLoud />
          <input
            type="range"
            max={1}
            min={0}
            step={0.02}
            value={volume}
            onChange={volumeBarChange}
          />
        </div>
        <div className="row">
          <div className="col-auto">
            <p>{formatTime(currentTime)}</p>
          </div>
          <div className="col">
            <input
              type="range"
              max={songDuration}
              min={0}
              step={0.02}
              value={currentTime}
              className="form-range"
            />
          </div>
          <div className="col-auto">
            <p>{formatTime(songDuration)}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PlayButton;
