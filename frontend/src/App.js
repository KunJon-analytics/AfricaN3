import { useEffect, useState } from "react";

import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "react-toastify/dist/ReactToastify.css";

import { ToastContainer } from "react-toastify";

import { NavBar } from "./components/NavBar";
import { Banner } from "./components/Banner";
import { Skills } from "./components/Skills";
import { Projects } from "./components/Projects";
import { Footer } from "./components/Footer";
import Wordle from "./components/Wordle";
import axiosInstance from "./api/axiosInstance";

function App() {
  const [solution, setSolution] = useState(null);

  const [wordleData, setWordleData] = useState([]);

  useEffect(() => {
    axiosInstance.get("words/").then((res) => {
      setWordleData(res.data);
      setSolution(res.data.word.content);
    });
  }, [setWordleData]);

  return (
    <div className="App">
      <NavBar />
      <ToastContainer />
      <Banner />
      <Skills />
      {solution && <Wordle solution={solution} />}
      <Projects />
      <Footer />
    </div>
  );
}

export default App;
