import React, { useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Modal from "react-bootstrap/Modal";
import InputGroup from "react-bootstrap/InputGroup";
import { sc, wallet } from "@cityofzion/neon-js";
import { helpers } from "@cityofzion/props";
import { useWallet } from "@rentfuse-labs/neo-wallet-adapter-react";
import { toast } from "react-toastify";
import { WitnessScope } from "@rentfuse-labs/neo-wallet-adapter-base";
import axiosInstance from "../api/axiosInstance";
import {
  nodeUrl,
  factor,
  magpieContractAddress,
  gasContractAddress,
} from "../utils/constants";
import { CirclesWithBar, Puff } from "react-loader-spinner";
import { Formik } from "formik";
import { object, string, number } from "yup";

let wordleSchema = object({
  title: string().required().max(60),
  description: string().required().max(120),
  reward: number().required().positive().min(1),
  no_of_words: number()
    .required("Number of rounds for the game is required")
    .positive()
    .integer()
    .min(1, "At least one round is required for each game")
    .max(7, "The maximum number of rounds per game is 7"),
  search_twitter: string()
    .matches(
      /^[a-zA-Z0-9_#$]+$/,
      "Just one word is required. $ and # are the only special characters allowed"
    )
    .required("Please type in search keyword"),
});

export default function CreateWordle({ show, setShow }) {
  const { address, invoke } = useWallet();
  const [stage, setStage] = useState("starting");

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const handleQuizCreateForm = async (data) => {
    try {
      handleClose();
      let formData = new FormData();
      formData.append("title", data.title);
      formData.append("description", data.description);
      formData.append("reward", data.reward);
      formData.append("no_of_words", data.no_of_words);
      formData.append("search_twitter", data.search_twitter);

      // Construct the request and invoke it
      let amount = data.reward * factor;
      let trivia_type = sc.ContractParam.byteArray("wordle");
      let winners_no = sc.ContractParam.integer(data.no_of_words);
      let data_array = [trivia_type, winners_no];

      let param = {
        scriptHash: gasContractAddress,
        operation: "transfer",
        args: [
          {
            type: "Hash160",
            value: sc.ContractParam.hash160(address).toJson().value,
          },
          {
            type: "Hash160",
            value: sc.ContractParam.hash160(magpieContractAddress).toJson()
              .value,
          },
          {
            type: "Integer",
            value: sc.ContractParam.integer(amount).toJson().value,
          },
          {
            type: "Array",
            value: sc.ContractParam.array(...data_array).toJson().value,
          },
        ],
        signers: [
          {
            account: wallet.getScriptHashFromAddress(address),
            scopes: WitnessScope.CalledByEntry,
          },
        ],
      };

      const result = await invoke(param);

      if (result.data?.txId) {
        toast.info(
          `🦄 Waiting for transaction confirmation, please stay on this page`,
          {
            position: "top-right",
            autoClose: 25000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: false,
            draggable: true,
            progress: undefined,
          }
        );
        console.log("sleeping...");
        setStage("blockchain");
        await helpers.sleep(25000);
        setStage("API");
        let events = await helpers.getEvents(nodeUrl, result.data?.txId);
        if (events.length) {
          const triviaId = JSON.stringify(events[3].value[0]);
          toast.success(`🦄 New Wordle game created with ID: ${triviaId}!`, {
            position: "top-right",
            autoClose: 3500,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: false,
            draggable: true,
            progress: undefined,
          });
          formData.append("wordle_id", triviaId);
          formData.append("master", address);
          formData.append("transaction_id", result.data?.txId);
          setStage("starting");
          axiosInstance
            .post(`words/create/`, formData)
            .then((res) => {
              console.log(res);
              toast.success(
                `🦄 Wordle game with: ID: ${res.data.id} was successfully created!`,
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
      }
    } catch (error) {
      toast.error("An error occurred while creating the wordle game", {
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
      console.error("An error occurred while creating the wordle game");
    }
  };

  return (
    <>
      <Button variant="dark" onClick={handleShow}>
        Create Wordle
      </Button>

      <CirclesWithBar
        height="100"
        width="100"
        color="#4fa94d"
        wrapperStyle={{}}
        wrapperClass="loader"
        visible={stage === "blockchain"}
        outerCircleColor=""
        innerCircleColor=""
        barColor=""
        ariaLabel="circles-with-bar-loading"
      />

      <Puff
        height="80"
        width="80"
        radisu={1}
        color="#4fa94d"
        ariaLabel="puff-loading"
        wrapperStyle={{}}
        wrapperClass="loader"
        visible={stage === "API"}
      />

      <Modal show={show} onHide={handleClose} centered>
        <Modal.Header className="createmodal">
          <Modal.Title>Create a Wordle Game</Modal.Title>
        </Modal.Header>
        <Modal.Body className="createmodal">
          <Formik
            validationSchema={wordleSchema}
            onSubmit={(data) => handleQuizCreateForm(data)}
            initialValues={{
              title: "",
              description: "",
              reward: 10,
              no_of_words: 5,
              search_twitter: "",
            }}
          >
            {({ handleSubmit, handleChange, values, touched, errors }) => (
              <Form noValidate onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="validationFormik01">
                  <Form.Label>Title</Form.Label>
                  <Form.Control
                    type="text"
                    name="title"
                    value={values.title}
                    onChange={handleChange}
                    autoFocus
                    placeholder="A short game title"
                    isInvalid={!!errors.title}
                    isValid={touched.title && !errors.title}
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.title}
                  </Form.Control.Feedback>
                  <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                </Form.Group>
                <Form.Group className="mb-3" controlId="validationFormik02">
                  <Form.Label>Description</Form.Label>
                  <Form.Control
                    type="text"
                    name="description"
                    value={values.description}
                    onChange={handleChange}
                    autoFocus
                    placeholder="An interesting description of this game"
                    isInvalid={!!errors.description}
                    isValid={touched.description && !errors.description}
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.description}
                  </Form.Control.Feedback>
                  <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                </Form.Group>
                <Form.Group className="mb-3" controlId="validationFormikReward">
                  <Form.Label>Reward</Form.Label>
                  <InputGroup hasValidation>
                    <InputGroup.Text id="inputGroupPrepend">
                      $GAS
                    </InputGroup.Text>
                    <Form.Control
                      type="number"
                      placeholder="10"
                      aria-describedby="rewardHelpBlock"
                      name="reward"
                      value={values.reward}
                      onChange={handleChange}
                      isInvalid={!!errors.reward}
                    />
                    <Form.Control.Feedback type="invalid">
                      {errors.reward}
                    </Form.Control.Feedback>
                  </InputGroup>
                  <Form.Text id="rewardHelpBlock" muted>
                    The total $GAS reward to be shared among winners
                  </Form.Text>
                </Form.Group>
                <Form.Group
                  className="mb-3"
                  controlId="validationFormikWordsNumber"
                >
                  <Form.Label>Number of Rounds</Form.Label>
                  <InputGroup hasValidation>
                    <Form.Control
                      type="number"
                      placeholder="5"
                      aria-describedby="numberOfWordsHelpBlock"
                      name="no_of_words"
                      value={values.no_of_words}
                      onChange={handleChange}
                      isInvalid={!!errors.no_of_words}
                    />
                    <Form.Control.Feedback type="invalid">
                      {errors.no_of_words}
                    </Form.Control.Feedback>
                  </InputGroup>
                  <Form.Text id="numberOfWordsHelpBlock" muted>
                    The number of rounds in this game.
                  </Form.Text>
                </Form.Group>
                <Form.Group
                  className="mb-3"
                  controlId="validationFormikSearchTwitter"
                >
                  <Form.Label>Search Twitter</Form.Label>
                  <Form.Control
                    type="text"
                    name="search_twitter"
                    value={values.search_twitter}
                    onChange={handleChange}
                    autoFocus
                    aria-describedby="searchTwitterHelpBlock"
                    placeholder=""
                    isValid={touched.search_twitter && !errors.search_twitter}
                    isInvalid={!!errors.search_twitter}
                  />
                  <Form.Text id="searchTwitterHelpBlock" muted>
                    A keyword to search twitter with. Examples: $NEO, #NEO,
                    Hongfei
                  </Form.Text>
                  <Form.Control.Feedback type="invalid">
                    {errors.search_twitter}
                  </Form.Control.Feedback>
                  <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                </Form.Group>
                <Button type="submit" variant="primary">
                  Save Changes
                </Button>
              </Form>
            )}
          </Formik>
        </Modal.Body>
        <Modal.Footer className="createmodal">
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
