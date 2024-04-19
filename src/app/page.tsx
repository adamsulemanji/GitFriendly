"use client";

import React from "react";
import "../styles/Home.module.css";
import axios from "axios";
import { ChakraProvider } from "@chakra-ui/react";
import { useToast } from "@chakra-ui/react";

export default function Home() {
  const [url, setUrl] = React.useState<string>("");
  const [data, setData] = React.useState<string>("");
  const toast = useToast();

  function handleUrlChange(event: React.ChangeEvent<HTMLInputElement>) {
    setUrl(event.target.value);
  }

  function checkUrl(url: string) {
    return url.includes("github.com") && url.startsWith("https://");
  }

  async function handleSubmit(event: React.ChangeEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!url) {
      toast({
        title: "No URL",
        description: "Please enter a URL",
        status: "error",
        duration: 9000,
        isClosable: true
      });
      return;
    }

    if (!checkUrl(url)) {
      toast({
        title: "Invalid URL",
        description: "Please enter a valid Github URL",
        status: "error",
        duration: 9000,
        isClosable: true
      });
      return;
    }

    axios
      .post("http://127.0.0.1:5000/clean", { url })
      .then((response) => {
        console.log(response.data);
        if (response.data) {
          toast({
            title: "URL Submitted",
            description: "We are cleaning the data for you",
            status: "info",
            duration: 9000,
            isClosable: true
          });
        }
      })
      .catch((error) => {
        console.error(error);
      });
  }

  return (
    <ChakraProvider>
      <div className="flex min-h-screen flex-col items-center justify-center bg-gray-200">
        <div className="flex flex-col items-center justify-center w-full flex-1 px-20 text-center">
          <h1 className="text-6xl font-bold mb-8 bg-clip-text text-transparent bg-gradient-to-r from-custom-blue via-custom-orange to-custom-red hover:from-custom-red hover:via-custom-orange hover:to-custom-blue transition-all duration-1000">
            GitFriendly
          </h1>

          <form className="flex w-full max-w-5xl" onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Enter a Github Link..."
              className="w-full px-4 py-2 border rounded-3xl shadow-md focus:outline-none focus:border-custom-blue text-black"
              value={url}
              onChange={handleUrlChange}
            />
            <button className="ml-4 px-6 py-2 text-white bg-custom-blue hover:bg-custom-orange rounded-full focus:outline-none focus:ring transition-all duration-500">
              Search
            </button>
          </form>
        </div>
        {data && <div>{data}</div>}
      </div>
    </ChakraProvider>
  );
}
