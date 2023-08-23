import { FaHome, FaBook, FaFileAlt, FaIcons } from "react-icons/fa";
import { RiOpenaiFill } from "react-icons/ri";
import { BsChatLeft } from "react-icons/bs";
import {
  Box,
  Button,
  HStack,
  IconButton,
  Tooltip,
  useDisclosure,
  VStack,
  Text,
  Heading,
  Center,
  SimpleGrid,
  GridItem,
  Grid,
  useToast,
} from "@chakra-ui/react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import useUser from "../lib/userUser";
import { getDialogue } from "../api";
import Loading from "../components/Loading";
import Header from "../components/Header";
import { useRef, useState } from "react";

export default function Dialogues() {
  const { systemInfoPk } = useParams();
  const { isLoading, data } = useQuery<string[]>(
    ["dialogue", systemInfoPk],
    getDialogue
  );
  const toast = useToast();

  const copyToClipboard = (dialogue: string, index: number) => {
    navigator.clipboard.writeText(dialogue);
    toast({
      title: "Copied!",
      status: "success",
      duration: 1000,
      position: "bottom-right",
    });
  };

  return isLoading ? (
    <Loading />
  ) : (
    <VStack p="20" align="flex-start" w="80%">
      <Box p="4" fontSize="lg">
        <Text>아래의 텍스트을 순서대로 ChatGPT에게 보내면 됩니다.</Text>
        <Text color="whiteAlpha.700" fontSize="md">
          우측 상단의 복사 버튼을 클릭해서 복사할 수 있습니다.
        </Text>
      </Box>
      <Box p="4" fontSize="lg">
        <Text>
          텍스트의 내용은 선택한 System Information을 토대로 영어로 작성되었으며
          마지막에 선택한 언어로 답변하는 텍스트가 있습니다.
        </Text>
        <Text color="whiteAlpha.700" fontSize="md">
          전부 전달했을 시 마지막엔 선택한 언어로 답변이 나옵니다!
        </Text>
      </Box>
      <Heading ml="10" mt="20" mb="10" size="2xl">
        Scripts
      </Heading>
      <VStack justifyContent="flex-start" w="80%">
        {data?.map((dialogue, index: number) => (
          <HStack w="100%" key={index} my="10">
            <Center
              w="10%"
              background="whiteAlpha.300"
              boxSize="14"
              fontSize="2xl"
              display="flex"
              rounded="28"
            >
              {index + 1}
            </Center>
            <Box w="5%"></Box>
            <Box
              w="80%"
              background="blackAlpha.900"
              p="10"
              rounded="10"
              position="relative"
            >
              <Text>{dialogue}</Text>
              <IconButton
                icon={<FaBook />}
                aria-label="Copy"
                size="xs"
                color="white.100"
                background="whiteAlpha.400"
                position="absolute"
                top="5"
                right="5"
                transform="translate(50%, -50%)" // 아이콘을 정확한 중앙으로 위치시킵니다.
                onClick={() => copyToClipboard(dialogue, index)} // 클릭 이벤트 핸들러를 추가합니다.
              />
            </Box>
          </HStack>
        ))}
      </VStack>
    </VStack>
  );
}
