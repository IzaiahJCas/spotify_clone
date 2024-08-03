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

  // const audioVolume = (event) => {
  //   if (audioRef.current) {
  //     audioRef.current.volume = volume;
  //   }
  // };

  return (
    <Container fluid className="d-flex flex-column" style={{ height: "100vh" }}>
      <Row className="flex-grow-1">
        <Col className="border border-dark d-flex flex-column" xs={2} md={2}>
          <History
            currentSong={currentSong}
            songPlaying={songPlaying}
            songTitle={songTitle}
            setCurrentSong={setCurrentSong}
            setSongPlaying={setSongPlaying}
            setSongTitle={setSongTitle}
          />
        </Col>
        <Col className="border border-dark d-flex flex-column" xs={10} md={10}>
          <SearchBar songTitle={songTitle} />
        </Col>
      </Row>
      <Row className="border border-dark">
        <PlayButton
          playAndPause={playButton}
          currentSong={currentSong}
          songPlaying={songPlaying}
          audioRef={audioRef}
          volume={volume}
          setVolume={setVolume}
        />
      </Row>
    </Container>
  );
}

export default App;
