import { useContext } from "react";
import {
  WalletDisconnectButton,
  WalletMultiButton,
} from "@rentfuse-labs/neo-wallet-adapter-react-ui";
import { useWallet } from "@rentfuse-labs/neo-wallet-adapter-react";
import AuthContext from "../context/AuthContext";

const ButtonConnect = () => {
  const { user } = useContext(AuthContext);
  const { connected } = useWallet();
  console.log(user);
  console.log(connected);
  if (!connected) {
    return <WalletMultiButton size={"small"} className="vvd" />;
  } else {
    return <WalletDisconnectButton size={"small"} className="vvd" />;
  }
};

export default ButtonConnect;
