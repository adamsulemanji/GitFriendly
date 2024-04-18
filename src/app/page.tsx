"use client";

import React from "react";
import "../styles/Home.module.css";

export default function Home() {
  const [url, setUrl] = React.useState<string>("");

  function handleUrlChange(event: React.ChangeEvent<HTMLInputElement>) {
    setUrl(event.target.value);
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
  }

  return (
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
    </div>
  );
}
