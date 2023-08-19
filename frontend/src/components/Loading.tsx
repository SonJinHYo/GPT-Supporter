import { AddIcon, SpinnerIcon } from "@chakra-ui/icons";
import { Button, Heading, Spinner, Text, VStack } from "@chakra-ui/react";

export default function Loading() {
  return (
    <VStack bg="gray.800" justifyContent={"center"} minH="70vh">
      <Heading mb={6} size="2xl">
        Loading . . .
      </Heading>
      <Spinner size="lg" />
    </VStack>
  );
}
