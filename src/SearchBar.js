import { Col, Container, Row } from "react-bootstrap";
import { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

function SearchBar() {
  const [songName, setSongName] = useState("");

  const handleSubmit = (e) => {
    fetch("YoutubeAudioDownload", {
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify({ songName: songName }),
    });
  };

  const handleTyping = (e) => {
    setSongName(e.target.value);
    console.log(songName);
  };

  return (
    <Container>
      <form onSubmit={handleSubmit}>
        <label htmlFor="song-search">Find your song:</label>
        <Row>
          <Col>
            <input
              className="form-control"
              id="song-search"
              type="text"
              onChange={handleTyping}
            />
          </Col>
          <Col>
            <button type="submit">Search</button>
          </Col>
        </Row>
      </form>
    </Container>
  );
}

export default SearchBar;
