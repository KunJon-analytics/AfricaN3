import {
  WalletDisconnectButton,
  WalletMultiButton,
} from "@rentfuse-labs/neo-wallet-adapter-react-ui";
import { useWallet } from "@rentfuse-labs/neo-wallet-adapter-react";

const ButtonConnect = () => {
  const { connected } = useWallet();
  if (!connected) {
    return <WalletMultiButton size={"small"} className="vvd" />;
  } else {
    return <WalletDisconnectButton size={"small"} className="vvd" />;
  }
};

export default ButtonConnect;
