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
  setCurrentVideo,
  currentVideo,
  setVideoPlaying,
  videoPlaying,
}) {
  return (
    <div class="h-full">
      <SongList
        currentSong={currentSong}
        songPlaying={songPlaying}
        songTitle={songTitle}
        setCurrentSong={setCurrentSong}
        setSongPlaying={setSongPlaying}
        setSongTitle={setSongTitle}
        videoPlaying={videoPlaying}
        currentVideo={currentVideo}
        setCurrentVideo={setCurrentVideo}
        setVideoPlaying={setVideoPlaying}
      />
    </div>
  );
}

export default History;
