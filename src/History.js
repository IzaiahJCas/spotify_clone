import { Col, Container, Row } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import SongList from "./components/SongList";
function History({
  currentSong,
  setCurrentSong,
  songPlaying,
  setSongPlaying,
  songTitle,
  setSongTitle,
}) {
  return (
    <Container style={{ display: "flex", flexDirection: "column", flex: "1" }}>
      <SongList
        currentSong={currentSong}
        songPlaying={songPlaying}
        songTitle={songTitle}
        setCurrentSong={setCurrentSong}
        setSongPlaying={setSongPlaying}
        setSongTitle={setSongTitle}
      />
    </Container>
  );
}

export default History;
