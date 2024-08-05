import { Col, Container, Row } from "react-bootstrap";
import { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./SearchBar.css";

function SearchBar({ songTitle }) {
  const [amount, setAmount] = useState("");
  const [artist, setArtist] = useState("");
  const [name, setName] = useState("");

  console.log("Amount:", amount);
  console.log("Artist:", artist);
  console.log("Name:", name);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("/submit_form", {
        method: "POST",
        headers: {
          "content-type": "application/json",
        },
        body: JSON.stringify({ amount: amount, artist: artist, name: name }),
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
      <form onSubmit={handleSubmit}>
        <Row className="center-items">
          <Col className="mt-3">
            <input
              className="form-control custom-input"
              id="song-amount"
              type="text"
              value={amount}
              placeholder="Amount of songs: "
              onChange={(e) => setAmount(e.target.value)}
            />
          </Col>
          <Col className="mt-3">
            <input
              className="form-control custom-input"
              id="song-artist"
              value={artist}
              placeholder="Song Artist: "
              type="text"
              onChange={(e) => setArtist(e.target.value)}
            />
          </Col>
          <Col className="mt-3">
            <input
              className="form-control custom-input"
              id="song-name"
              value={name}
              placeholder="Song Name: "
              type="text"
              onChange={(e) => setName(e.target.value)}
            />
          </Col>
          <Col>
            <button
              type="submit"
              className="text-red-500 rounded-md border-2 border-red-500 p-2 mt-3.5 mb-2 hover:bg-white transition-colors duration-300"
            >
              Search
            </button>
          </Col>
        </Row>
      </form>
      <Row className="text-white text-2xl custom-text">
        <h1>Song Playing: {songTitle}</h1>
      </Row>
    </Container>
  );
}

export default SearchBar;
