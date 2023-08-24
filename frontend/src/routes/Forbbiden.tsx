import { Button, Heading, Text, VStack } from "@chakra-ui/react";
import { Link } from "react-router-dom";

export default function Forbidden() {
  return (
    <VStack bg="gray.800" justifyContent={"center"} minH="70vh">
      <Heading fontSize="5xl">권한이 없습니다.</Heading>
      <Text>로그인 후 이용해주세요</Text>
      <Link to="/">
        <Button colorScheme={"red"} variant={"link"}>
          Go home &rarr;
        </Button>
      </Link>
    </VStack>
  );
}
