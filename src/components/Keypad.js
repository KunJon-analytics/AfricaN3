import React, { useEffect, useState } from "react";
import axiosInstance from "../api/axiosInstance";
import Alphabets from "./Alphabets";

export default function Keypad({ usedKeys, handleClick }) {
  const [letters, setLetters] = useState(null);

  useEffect(() => {
    axiosInstance.get("words/letters/").then((res) => {
      setLetters(res.data);
    });
  }, []);

  return (
    <div className="keypad">
      {letters && (
        <Alphabets
          letters={letters}
          usedKeys={usedKeys}
          handleClick={handleClick}
        />
      )}
      <div className="action" onClick={handleClick}>
        Delete
      </div>
      <div className="action" onClick={handleClick}>
        Enter
      </div>
    </div>
  );
}
