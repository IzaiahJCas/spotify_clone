import { Col, Container, Row } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { useState, useEffect, useRef } from "react";
import SearchBar from "./SearchBar";
import History from "./History";
import PlayButton from "./PlayButton";
import "./App.css";

function App() {
  const [currentSong, setCurrentSong] = useState(null);
  const [songPlaying, setSongPlaying] = useState(null);
  const [currentVideo, setCurrentVideo] = useState(null);
  const [videoPlaying, setVideoPlaying] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [songTitle, setSongTitle] = useState(null);
  const [volume, setVolume] = useState(0);
  const audioRef = useRef(null);
  const videoRef = useRef(null);

  const playButton = () => {
    if (audioRef.current && videoRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
        videoRef.current.pause();
      } else {
        audioRef.current.play();
        videoRef.current.play();
      }
      setIsPlaying(!isPlaying);
    } else if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    } else if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  return (
    <div class=" bg-slate-950 h-screen">
      <div class="grid grid-rows-8 grid-cols-5 gap-4 h-screen">
        {/*top row*/}
        <div class="border-2 border-blue-800/10 bg-white/10 backdrop-blur-xl custom-scrollbar col-span-2 row-span-7 rounded-lg shadow-custom-shadow h-51 mt-4 mb-4 ml-4">
          <History
            currentSong={currentSong}
            songPlaying={songPlaying}
            songTitle={songTitle}
            videoPlaying={videoPlaying}
            currentVideo={currentVideo}
            setCurrentSong={setCurrentSong}
            setSongPlaying={setSongPlaying}
            setSongTitle={setSongTitle}
            setCurrentVideo={setCurrentVideo}
            setVideoPlaying={setVideoPlaying}
          />
        </div>
        <div class="border-2 border-blue-800/10 bg-white/10 backdrop-blur-xl col-span-3 row-span-7 rounded-lg shadow-custom-shadow h-51 mt-4 mb-4 mr-4">
          <SearchBar
            songTitle={songTitle}
            videoPlaying={videoPlaying}
            currentVideo={currentVideo}
            setCurrentVideo={setCurrentVideo}
            setVideoPlaying={setVideoPlaying}
            videoRef={videoRef}
          />
        </div>
        {/*bottom row*/}
        <div class="col-span-5 grid grid-rows-subgrid gap-4 row-span-1 bg-black/80 mt">
          <PlayButton
            playAndPause={playButton}
            currentSong={currentSong}
            songPlaying={songPlaying}
            audioRef={audioRef}
            videoRef={videoRef}
            volume={volume}
            setVolume={setVolume}
            currentVideo={currentVideo}
            videoPlaying={videoPlaying}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
