import { Box } from "@chakra-ui/react";
import { Outlet } from "react-router-dom";
import { Helmet } from "react-helmet";

import Header from "./Header";
export default function Root() {
  return (
    <Box>
      <Helmet>
        <title>GPT Supporter</title>
      </Helmet>
      <Header />
      <Outlet />
    </Box>
  );
}
