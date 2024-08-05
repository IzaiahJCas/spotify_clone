import { Col, Container, Row } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { useState, useEffect, useRef } from "react";
import SearchBar from "./SearchBar";
import History from "./History";
import PlayButton from "./PlayButton";
import "./App.css";

function App() {
  const [audioList, setAudioList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentSong, setCurrentSong] = useState(null);
  const [songPlaying, setSongPlaying] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [songTitle, setSongTitle] = useState(null);
  const [volume, setVolume] = useState(0);
  const audioRef = useRef(null);

  const playButton = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.play();
        setIsPlaying(false);
      } else {
        audioRef.current.pause();
        setIsPlaying(true);
      }
    }
  };

  return (
    <div class=" bg-black h-screen">
      <div class="grid grid-rows-8 grid-cols-5 gap-4 h-screen">
        {/*top row*/}
        <div class="custom-scrollbar col-span-1 row-span-7 bg-background-grey rounded-lg shadow-custom-shadow h-51 mt-4 mb-4 ml-4">
          <History
            currentSong={currentSong}
            songPlaying={songPlaying}
            songTitle={songTitle}
            setCurrentSong={setCurrentSong}
            setSongPlaying={setSongPlaying}
            setSongTitle={setSongTitle}
          />
        </div>
        <div class="col-span-4 row-span-7 bg-background-grey rounded-lg shadow-custom-shadow h-51 mt-4 mb-4 mr-4">
          <SearchBar songTitle={songTitle} />
        </div>
        {/*bottom row*/}
        <div class="col-span-5 grid grid-rows-subgrid gap-4 row-span-1 bg-black mt">
          <PlayButton
            playAndPause={playButton}
            currentSong={currentSong}
            songPlaying={songPlaying}
            audioRef={audioRef}
            volume={volume}
            setVolume={setVolume}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
