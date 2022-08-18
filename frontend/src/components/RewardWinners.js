import Carousel from "react-multi-carousel";
import payment from "../assets/img/payment.png";
import "react-multi-carousel/lib/styles.css";
import colorSharp from "../assets/img/color-sharp.png";

export const RewardWinners = ({ unpaid, setUnpaid }) => {
  const responsive = {
    superLargeDesktop: {
      // the naming can be any, depends on you.
      breakpoint: { max: 4000, min: 3000 },
      items: 5,
    },
    desktop: {
      breakpoint: { max: 3000, min: 1024 },
      items: 3,
    },
    tablet: {
      breakpoint: { max: 1024, min: 464 },
      items: 2,
    },
    mobile: {
      breakpoint: { max: 464, min: 0 },
      items: 1,
    },
  };

  return (
    <section className="skill" id="community">
      <div className="container">
        <div className="row">
          <div className="col-12">
            <div className="skill-bx wow zoomIn">
              <h2>Unclaimed Rewards</h2>
              <p>
                There are {unpaid?.length} unpaid game(s) left.<br></br> Click
                on the image below to release the reward to winners.
              </p>
              <Carousel
                responsive={responsive}
                infinite={true}
                className="owl-carousel owl-theme skill-slider"
              >
                {unpaid?.map((win) => (
                  <div
                    key={win.id}
                    className="item"
                    onClick={() => console.log("clicked")}
                  >
                    <img src={payment} alt="Image" />
                    <h5>
                      {win.no_of_words} Winner{win.no_of_words > 1 ? "s" : ""}
                    </h5>
                  </div>
                ))}
              </Carousel>
            </div>
          </div>
        </div>
      </div>
      <img className="background-image-left" src={colorSharp} alt="Image" />
    </section>
  );
};
