import React from "react";

export default function Modal({ isCorrect, solution, turn }) {
  return (
    <div className="result">
      {isCorrect && (
        <div className="polygon">
          <h2>You Win!</h2>
          <p className="solution">{solution}</p>
          <p>You found the solution in {turn} guesses :)</p>
        </div>
      )}
      {!isCorrect && (
        <div className="polygon">
          <h2>Nevermind</h2>
          <p>Better luck next time :)</p>
        </div>
      )}
    </div>
  );
}
