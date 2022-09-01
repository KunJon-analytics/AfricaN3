import { Container, Row, Col } from "react-bootstrap";
import headerImg from "../assets/img/avatar.png";
import { ArrowRightCircle } from "react-bootstrap-icons";
import "animate.css";
import TrackVisibility from "react-on-screen";
import { TypingComponent } from "./Typing";

export const Banner = ({ solution }) => {
  function NewTab() {
    window.open(
      "https://medium.com/@rmgura16/introducing-neo-wordle-d0b0c47b59d6",
      "_blank"
    );
  }
  return (
    <section className="banner" id="home">
      <Container>
        <Row className="aligh-items-center">
          <Col xs={12} md={6} xl={7}>
            <TrackVisibility>
              {({ isVisible }) => (
                <div
                  className={
                    isVisible ? "animate__animated animate__fadeIn" : ""
                  }
                >
                  <span className="tagline">Welcome to AfricaN3</span>
                  <h1>
                    {`We love`}{" "}
                    <span
                      className="txt-rotate"
                      data-rotate='[ "the Smart Economy", "the Metaverse", "DeFi" ]'
                    >
                      <span className="wrap">
                        {solution ? (
                          <span className="wrap">the Smart Economy</span>
                        ) : (
                          <TypingComponent className="wrap" />
                        )}
                      </span>{" "}
                    </span>
                  </h1>
                  <p>
                    A vibrant community that helps expose African talents to the
                    NEO blockchain and assist them transition into value
                    creators in the ecosystem.
                  </p>
                  <button onClick={() => NewTab()}>
                    Play2Earn <ArrowRightCircle size={25} />
                  </button>
                </div>
              )}
            </TrackVisibility>
          </Col>
          <Col xs={12} md={6} xl={5}>
            <TrackVisibility>
              {({ isVisible }) => (
                <div
                  className={
                    isVisible ? "animate__animated animate__zoomIn" : ""
                  }
                >
                  <img src={headerImg} alt="Header Img" />
                </div>
              )}
            </TrackVisibility>
          </Col>
        </Row>
      </Container>
    </section>
  );
};
