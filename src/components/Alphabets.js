import React from "react";

const Alphabets = ({ letters, usedKeys, handleClick }) => {
  return letters.map((l) => {
    const color = usedKeys[l.key];
    return (
      <div key={l.key} className={color} onClick={handleClick}>
        {l.key}
      </div>
    );
  });
};

export default Alphabets;
