import { Col, Container, Row } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { useState, useEffect } from "react";
import SearchBar from "./SearchBar";
import History from "./History";
import PlayButton from "./PlayButton";
import "./App.css";

function App() {
  return (
    <Container fluid className="d-flex flex-column" style={{ height: "100vh" }}>
      <Row className="flex-grow-1">
        <Col className="border border-dark d-flex flex-column" xs={2} md={2}>
          <History />
        </Col>
        <Col className="border border-dark d-flex flex-column" xs={10} md={10}>
          <SearchBar />
        </Col>
      </Row>
      <Row className="border border-dark">
        <PlayButton />
      </Row>
    </Container>
  );
}

export default App;
