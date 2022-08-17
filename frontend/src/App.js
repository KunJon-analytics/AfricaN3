import { useEffect, useState, useContext } from "react";

import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "react-toastify/dist/ReactToastify.css";

import { ToastContainer } from "react-toastify";
import { useWallet } from "@rentfuse-labs/neo-wallet-adapter-react";

import { NavBar } from "./components/NavBar";
import AuthContext from "./context/AuthContext";
import { Banner } from "./components/Banner";
import { Skills } from "./components/Skills";
import { Projects } from "./components/Projects";
import { Footer } from "./components/Footer";
import Wordle from "./components/Wordle";
import axiosInstance from "./api/axiosInstance";
import { register } from "./utils/auth";

function App() {
  const { user } = useContext(AuthContext);
  const { address, connected, invoke } = useWallet();
  const [sameWallet, setSameWallet] = useState(false);
  const [solution, setSolution] = useState(null);

  const [wordleData, setWordleData] = useState({});

  useEffect(() => {
    if (connected && !user) {
      register(address);
    } else if (connected && address == user.wallet_address) {
      setSameWallet(true);
    } else {
      setSameWallet(false);
      setSolution(null);
    }
  }, [connected, address, user]);

  useEffect(() => {
    if (sameWallet) {
      axiosInstance.get("words/").then((res) => {
        setWordleData(res.data);
        setSolution(res.data.word.content);
      });
    }
  }, [setWordleData, sameWallet]);

  console.log(wordleData)

  return (
    <div className="App">
      <NavBar />
      <ToastContainer />
      <Banner />
      <Skills />
      {solution && <Wordle solution={solution} wordleData={wordleData} />}
      <Projects />
      <Footer />
    </div>
  );
}

export default App;
