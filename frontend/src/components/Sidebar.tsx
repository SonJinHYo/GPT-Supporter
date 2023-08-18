import React, { useState } from "react";
import {
  ChakraProvider,
  CSSReset,
  Box,
  Flex,
  VStack,
  IconButton,
  Button,
  Text,
  extendTheme,
  Slide,
  useDisclosure,
} from "@chakra-ui/react";
import { motion, Variants } from "framer-motion";
import { ChevronLeftIcon, ChevronRightIcon } from "@chakra-ui/icons";

const theme = extendTheme({
  fonts: {
    body: "'Helvetica Neue', sans-serif",
    heading: "'Helvetica Neue', sans-serif",
  },
});
const MotionVStack = motion(VStack);

export default function Sidebar() {
  //   const [isOpen, setIsOpen] = useState(true);
  const { isOpen, onToggle } = useDisclosure();

  return (
    <Flex>
      {isOpen ? (
        <Slide direction="left" in={isOpen} style={{ zIndex: 10 }}>
          <VStack
            w="250px"
            bg="blue.500"
            color="white"
            height="100vh"
            alignItems="flex-start"
            padding="4"
            overflow="hidden"
          >
            <IconButton
              icon={<ChevronLeftIcon />}
              aria-label="Toggle Sidebar"
              variant="ghost"
              onClick={onToggle}
              alignSelf="flex-end"
            />
            <Button variant="link" color="white">
              메뉴 항목 1
            </Button>
            <Button variant="link" color="white">
              메뉴 항목 2
            </Button>
            <Button variant="link" color="white">
              메뉴 항목 3
            </Button>
          </VStack>
        </Slide>
      ) : (
        <IconButton
          icon={<ChevronRightIcon />}
          aria-label="Toggle Sidebar"
          onClick={onToggle}
          m="4"
        />
      )}
    </Flex>
  );
}
