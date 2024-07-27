import { Col, Container, Row } from "react-bootstrap";
import { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

function SearchBar() {
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
        <Row>
          <Col>
            <label htmlFor="song-amount">Amount of songs:</label>
            <input
              className="form-control"
              id="song-amount"
              type="text"
              value={amount}
              placeholder="Amount of songs: "
              onChange={(e) => setAmount(e.target.value)}
            />
          </Col>
          <Col>
            <label htmlFor="song-artist">Song Artist:</label>
            <input
              className="form-control"
              id="song-artist"
              value={artist}
              placeholder="Song Artist: "
              type="text"
              onChange={(e) => setArtist(e.target.value)}
            />
          </Col>
          <Col>
            <label htmlFor="song-name">Song Name:</label>
            <input
              className="form-control"
              id="song-name"
              value={name}
              placeholder="Song Name: "
              type="text"
              onChange={(e) => setName(e.target.value)}
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
