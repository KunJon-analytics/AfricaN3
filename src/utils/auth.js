import axiosInstance from "../api/axiosInstance";
import { shortenAddress } from "../utils/shortenAddress";

export const login = (address) => {
  axiosInstance
    .post(`token/`, {
      wallet_address: address,
      password: shortenAddress(address),
    })
    .then((res) => {
      localStorage.setItem("access_token", res.data.access);
      localStorage.setItem("refresh_token", res.data.refresh);
      axiosInstance.defaults.headers["Authorization"] =
        "JWT " + localStorage.getItem("access_token");
      window.location.href = "/";
      // console.log(res);
      // console.log(res.data);
    })
    .catch((error) => {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
        // http.ClientRequest in node.js
        console.log(error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log("Error", error.message);
      }
    });
};

export const register = (wallet_address) => {
  axiosInstance
    .post(`user/register/`, {
      wallet_address: wallet_address,
      password: shortenAddress(wallet_address),
    })
    .then((res) => {
      login(wallet_address);
      console.log(res);
      console.log(res.data);
    })
    .catch((error) => {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        if (
          error.response.data?.wallet_address[0] ===
          "custom user with this wallet address already exists."
        ) {
          login(wallet_address);
        }
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
        // http.ClientRequest in node.js
        console.log(error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log("Error", error.message);
      }
    });
};
