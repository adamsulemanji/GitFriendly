"use client";

import React from "react";
import "../styles/Home.module.css";
import LoadingScreen from "@/components/LoadingScreen";
import axios from "axios";
import { ChakraProvider } from "@chakra-ui/react";
import { useToast } from "@chakra-ui/react";

export default function Home() {
  const [url, setUrl] = React.useState<string>("");
  const [isLoading, setIsLoading] = React.useState<boolean>(false);
  const toast = useToast();

  function handleUrlChange(event: React.ChangeEvent<HTMLInputElement>) {
    setUrl(event.target.value);
  }

  function checkUrl(url: string) {
    return url.includes("github.com") && url.startsWith("https://");
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
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

    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
    }, 10000);
    axios
      .post("http://127.0.0.1:5000/clean", { url })
      .then((response) => {
        setIsLoading(false); // Stop loading
        if (response.data && response.data.modifiedHtml) {
          const blob = new Blob([response.data.modifiedHtml], {
            type: "text/html"
          });
          const url = URL.createObjectURL(blob);
          window.open(url, "_blank");
          toast({
            title: "URL Submitted",
            description: "Opening the cleaned data in a new tab.",
            status: "info",
            duration: 9000,
            isClosable: true
          });
        }
      })
      .catch((error) => {
        console.error(error);
        setIsLoading(false);
        toast({
          title: "Fetch Error",
          description: "Failed to fetch and process the URL",
          status: "error",
          duration: 9000,
          isClosable: true
        });
      });
  }

  return (
    <ChakraProvider>
      <div className="flex min-h-screen flex-col items-center justify-center bg-blue-50">
        {isLoading && <LoadingScreen />}
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
      </div>
    </ChakraProvider>
  );
}
