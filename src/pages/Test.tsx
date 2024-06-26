"use client";

import React, { useState } from "react";

export default function Test() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-200">
      <div className="flex flex-col items-center justify-center w-full flex-1 px-20 text-center">
        <button
          className="px-6 py-2 text-white bg-custom-blue hover:bg-custom-orange rounded-full focus:outline-none focus:ring transition-all duration-500"
          onClick={handleClick}
        >
          Click Me
        </button>
        <p className="text-4xl mt-4">{count}</p>
      </div>
    </div>
  );
}
