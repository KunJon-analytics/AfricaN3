import React, { useState, useEffect, useMemo } from "react";
import { WalletProvider } from "@rentfuse-labs/neo-wallet-adapter-react";
import logo from "../assets/img/whitelogo.png";
import {
  getNeoLineWallet,
  getO3Wallet,
  getWalletConnectWallet,
  getOneGateWallet,
} from "@rentfuse-labs/neo-wallet-adapter-wallets";
import { WalletModalProvider } from "@rentfuse-labs/neo-wallet-adapter-react-ui";

// Default styles that can be overridden by your app
require("@rentfuse-labs/neo-wallet-adapter-react-ui/styles.css");

const NWA = ({ children }) => {
  const getWallets = useMemo(() => {
    return [
      getNeoLineWallet(),
      getO3Wallet(),
      getOneGateWallet(),
      getWalletConnectWallet({
        options: {
          chains: ["neo3:testnet"], // ['neo3:mainnet', 'neo3:testnet', 'neo3:private']
          methods: [
            "invokeFunction",
            "testInvoke",
            "signMessage",
            "verifyMessage",
            "getapplicationlog",
          ],
          appMetadata: {
            name: "Magpie",
            description: "Create and Take Trivia to earn Tokens.",
            url: "https://magpie.space",
            icons: [logo],
          },
        },
        logger: "debug",
        relayProvider: "wss://relay.walletconnect.org",
      }),
    ];
  }, []);
  const [wallets, setWallets] = useState([]);

  useEffect(() => {
    setWallets(getWallets);
  }, [getWallets]);

  return (
    <>
      <WalletProvider wallets={wallets} autoConnect={false}>
        <WalletModalProvider centered={false} logo={logo} featuredWallets={3}>
          {children}
        </WalletModalProvider>
      </WalletProvider>
    </>
  );
};

export default NWA;
