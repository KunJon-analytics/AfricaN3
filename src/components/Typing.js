import { TypeAnimation } from "react-type-animation";

export const TypingComponent = () => {
  return (
    <TypeAnimation
      sequence={[
        "the Smart Economy", // Types 'One'
        2000, // Waits 1s
        "the Metaverse", // Deletes 'One' and types 'Two'
        2000, // Waits 2s
        "DeFi",
        2000,
      ]}
      wrapper="span"
      cursor={false}
      speed={45}
      repeat={Infinity}
      style={{ fontSize: "1em" }}
    />
  );
};
