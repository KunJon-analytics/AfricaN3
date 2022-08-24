import React, { useEffect, useState } from "react";
import axiosInstance from "../api/axiosInstance";

export default function Keypad({ usedKeys }) {
  const [letters, setLetters] = useState(null);

  useEffect(() => {
    axiosInstance.get("words/letters/").then((res) => {
      setLetters(res.data);
    });
  }, []);

  return (
    <div className="keypad">
      {letters &&
        letters.map((l) => {
          const color = usedKeys[l.key];
          return (
            <div key={l.key} className={color}>
              {l.key}
            </div>
          );
        })}
    </div>
  );
}
