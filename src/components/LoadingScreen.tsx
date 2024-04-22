"use client";

import React from "react";
import { Spinner, Box, Text } from "@chakra-ui/react";

function LoadingScreen() {
  return (
    <Box
      position="fixed"
      top="0"
      right="0"
      bottom="0"
      left="0"
      display="flex"
      justifyContent="center"
      alignItems="center"
      flexDirection="column"
      bg="white"
      zIndex="overlay"
    >
      <Spinner
        thickness="4px"
        speed="0.65s"
        emptyColor="gray.200"
        color="blue.500"
        size="xl"
      />
      <Text fontSize="lg" mt={3}>
        Loading...
      </Text>
    </Box>
  );
}

export default LoadingScreen;
