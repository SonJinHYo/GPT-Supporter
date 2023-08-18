import { Box, Button, HStack, VStack } from "@chakra-ui/react";
import { Link, Outlet } from "react-router-dom";
import { FaAirbnb } from "react-icons/fa";
import Sidebar from "./Sidebar";
import Header from "./Header";
export default function Root() {
  return (
    <Box>
      <Header />
      <Outlet />
    </Box>
  );
}
