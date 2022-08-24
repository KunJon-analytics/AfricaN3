import { useEffect, useState, useContext } from "react";

import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "react-toastify/dist/ReactToastify.css";

import { ToastContainer, toast } from "react-toastify";
import { useWallet } from "@rentfuse-labs/neo-wallet-adapter-react";

import { NavBar } from "./components/NavBar";
import AuthContext from "./context/AuthContext";
import { Banner } from "./components/Banner";
import { Skills } from "./components/Skills";
import { Projects } from "./components/Projects";
import { Footer } from "./components/Footer";
import { RewardWinners } from "./components/RewardWinners";
import Wordle from "./components/Wordle";
import axiosInstance from "./api/axiosInstance";
import { register } from "./utils/auth";
import { adminAddress } from "./utils/constants";

function App() {
  const { user } = useContext(AuthContext);
  const { address, connected } = useWallet();
  const [sameWallet, setSameWallet] = useState(false);
  const [solution, setSolution] = useState(null);
  const [unpaid, setUnpaid] = useState([]);

  const [wordleData, setWordleData] = useState({});

  useEffect(() => {
    if (connected && !user) {
      register(address);
    } else if (connected && address === user.wallet_address) {
      setSameWallet(true);
    } else {
      setSameWallet(false);
      setSolution(null);
      // add popup to show the wallet is different
    }
  }, [connected, address, user]);

  useEffect(() => {
    if (sameWallet) {
      axiosInstance
        .get("words/")
        .then((res) => {
          if (res.data) {
            setWordleData(res.data);
            setSolution(res.data.word.content);
          }
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
      axiosInstance.get("words/unpaid/").then((res) => {
        setUnpaid(res.data);
      });
    }
  }, [setWordleData, sameWallet]);

  const renderElement = () => {
    if (unpaid.length && connected && address === adminAddress) {
      return <RewardWinners unpaid={unpaid} setUnpaid={setUnpaid} />;
    } else {
      return <Skills />;
    }
  };

  return (
    <div className="App">
      <NavBar />
      <ToastContainer />
      <Banner />
      {renderElement()}
      {solution && <Wordle solution={solution} wordleData={wordleData} />}
      <Projects />
      <Footer />
    </div>
  );
}

export default App;
