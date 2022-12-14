import React, { useEffect, useState } from "react";
import { toast } from "react-toastify";
import useWordle from "../hooks/useWordle";
import CreateWordle from "./CreateWordle";
import axiosInstance from "../api/axiosInstance";
import { shortenAddress } from "../utils/shortenAddress";

// components
import Grid from "./Grid";
import Keypad from "./Keypad";
import Modal from "./Modal";

export default function Wordle({ solution, wordleData }) {
  const {
    currentGuess,
    guesses,
    turn,
    isCorrect,
    usedKeys,
    handleKeyup,
    history,
    handleClick,
  } = useWordle(solution);
  const [showModal, setShowModal] = useState(false);
  const [show, setShow] = useState(false);
  const reward = wordleData?.reward / wordleData?.no_of_words;

  useEffect(() => {
    window.addEventListener("keyup", handleKeyup);

    if (isCorrect) {
      setTimeout(() => setShowModal(true), 2000);
      window.removeEventListener("keyup", handleKeyup);
    }
    if (turn > 5) {
      setTimeout(() => setShowModal(true), 2000);
      window.removeEventListener("keyup", handleKeyup);
    }
    if (show) {
      window.removeEventListener("keyup", handleKeyup);
    }

    return () => window.removeEventListener("keyup", handleKeyup);
  }, [handleKeyup, isCorrect, turn, show]);

  useEffect(() => {
    if (showModal) {
      const submitSitting = () => {
        try {
          let presentWord = history.length ? history[history.length - 1] : null;
          let formData = new FormData();
          formData.append("word", wordleData.word.id);
          formData.append("passed", isCorrect);
          formData.append("word_guessed", presentWord);
          formData.append("attempts", turn);

          axiosInstance
            .post(`words/submit/`, formData)
            .then((res) => {
              console.log(res);
              toast.success(
                `🦄 Your submission was successful, come back tomorrow for another round`,
                {
                  position: "top-right",
                  autoClose: 8500,
                  hideProgressBar: false,
                  closeOnClick: true,
                  pauseOnHover: false,
                  draggable: true,
                  progress: undefined,
                }
              );
            })
            .catch((error) => {
              if (error.response) {
                // The request was made and the server responded with a status code
                // that falls out of the range of 2xx
                if (error.response.status === 429) {
                  toast.info("Come back tommorrow for another game round", {
                    position: "top-right",
                    autoClose: 3500,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                  });
                }
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
        } catch (error) {
          toast.error("An error occured during submission", {
            position: "top-right",
            autoClose: 3500,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
          });
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
          console.error("An error occured during submission");
        }
      };
      submitSitting();
    }
  }, [showModal]);

  return (
    <section className="wordle" id="wordle">
      <div className="wordle-bx">
        {solution && (
          <div>
            <h2>{`Win ${reward.toFixed(2)} $GAS`}</h2>
            <p>
              {`Game title: ${wordleData.title}`}
              <br></br> {`Master: ${shortenAddress(wordleData.master)}`}.
            </p>
            {!showModal && (
              <>
                <Grid
                  guesses={guesses}
                  currentGuess={currentGuess}
                  turn={turn}
                />
                <Keypad usedKeys={usedKeys} handleClick={handleClick} />
              </>
            )}
            {showModal && (
              <Modal isCorrect={isCorrect} turn={turn} solution={solution} />
            )}
          </div>
        )}
        <CreateWordle show={show} setShow={setShow} />
      </div>
    </section>
  );
}
