import Carousel from "react-multi-carousel";
import { toast } from "react-toastify";
import { WitnessScope } from "@rentfuse-labs/neo-wallet-adapter-base";
import { helpers } from "@cityofzion/props";
import { useWallet } from "@rentfuse-labs/neo-wallet-adapter-react";
import { sc, wallet } from "@cityofzion/neon-js";

import axiosInstance from "../api/axiosInstance";
import { nodeUrl, magpieContractAddress } from "../utils/constants";
import colorSharp from "../assets/img/color-sharp.png";
import payment from "../assets/img/payment.png";

export const RewardWinners = ({ unpaid, setUnpaid }) => {
  const { address, invoke } = useWallet();

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

  const sendTransaction = async (wordle_id, sittings, blockchain_id) => {
    let winners_list = sittings.filter((sitting) => sitting.winner);
    console.log(winners_list);
    try {
      // Construct the request and invoke it
      let raw_traits = winners_list?.map((winner) => {
        return sc.ContractParam.hash160(winner.user);
      });
      let param = {
        scriptHash: magpieContractAddress,
        operation: "createWinners",
        args: [
          {
            type: "Integer",
            value: sc.ContractParam.integer(blockchain_id).toJson().value,
          },
          {
            type: "Array",
            value: sc.ContractParam.array(...raw_traits).toJson().value,
          },
        ],
        signers: [
          {
            account: wallet.getScriptHashFromAddress(address),
            scopes: WitnessScope.CalledByEntry,
          },
        ],
      };
      console.log(raw_traits);
      console.log(param);
      const result = await invoke(param);
      // Optional: Wait for the transaction to be confirmed onchain
      if (result.data?.txId) {
        await helpers.sleep(30000);
        let new_result;
        new_result = await helpers.txDidComplete(
          nodeUrl,
          result.data?.txId,
          true
        );
        const published = new_result[0];
        if (!published) {
          toast.error("Winners were not published.", {
            position: "top-right",
            autoClose: 3500,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
          });
          console.error(`Winners were not published`);
          return;
        }
        let data = {
          transaction_id: result.data?.txId,
          wordle_id: wordle_id,
        };
        axiosInstance
          .post(`words/publish-winners/`, data)
          .then((res) => {
            console.log(res.data);
            toast.success("Winners successfully published", {
              position: "top-right",
              autoClose: 3500,
              hideProgressBar: false,
              closeOnClick: true,
              pauseOnHover: true,
              draggable: true,
              progress: undefined,
            });
            setUnpaid((prevState) =>
              prevState.filter((wordle) => wordle.id !== wordle_id)
            );
          })
          .catch((error) => {
            if (error.response) {
              // The request was made and the server responded with a status code
              // that falls out of the range of 2xx
              toast.error(error.response.data.detail, {
                position: "top-right",
                autoClose: 3500,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
              });
              console.log(error.response.data);
              console.log(error.response.status);
              console.log(error.response.headers);
            } else if (error.request) {
              // The request was made but no response was received
              // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
              // http.ClientRequest in node.js
              toast.error(error.request, {
                position: "top-right",
                autoClose: 3500,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
              });
              console.log(error.request);
            } else {
              // Something happened in setting up the request that triggered an Error
              toast.error(error.message, {
                position: "top-right",
                autoClose: 3500,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
              });
              console.log("Error", error.message);
            }
          });
      }
    } catch (error) {
      toast.error(
        "An error occurred while publishing the winners of the wordle game",
        {
          position: "top-right",
          autoClose: 3500,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
        }
      );
      toast.error(error.description, {
        position: "top-right",
        autoClose: 3500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
      console.error(error);
      console.error(
        "An error occurred while publishing the winners of the wordle game"
      );
    }
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
                    onClick={() =>
                      sendTransaction(win.id, win.sittings, win.wordle_id)
                    }
                  >
                    <img src={payment} alt="Unpaid winners" />
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
      <img
        className="background-image-left"
        src={colorSharp}
        alt="unpaid winner"
      />
    </section>
  );
};
