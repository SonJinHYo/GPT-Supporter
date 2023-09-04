import {
  Box,
  Button,
  Input,
  InputGroup,
  InputLeftElement,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalHeader,
  ModalOverlay,
  useToast,
  VStack,
  Text,
  IconButton,
  HStack,
  Center,
} from "@chakra-ui/react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { FaUser } from "react-icons/fa";
import { createRefBook, getPublicScriptDetail } from "../api";
import { MdTitle } from "react-icons/md";
import { CopyIcon } from "@chakra-ui/icons";
import { stringify } from "querystring";

interface IPublicScriptModalProps {
  isOpen: boolean;
  onClose: () => void;
  publicScriptPk: number;
}

interface IPublicScriptVariables {
  name: string;
  description: string;
  scripts: string[];
}

export default function RefBookModal({
  isOpen,
  onClose,
  publicScriptPk,
}: IPublicScriptModalProps) {
  const toast = useToast();

  const { isLoading, data, isError, error } = useQuery<IPublicScriptVariables>(
    ["public-scripts", publicScriptPk],
    () => getPublicScriptDetail(publicScriptPk)
  );

  console.log(data);

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast({
      title: "Copied!",
      status: "success",
      duration: 1000,
      position: "bottom-right",
    });
  };

  return (
    <Modal onClose={onClose} isOpen={isOpen}>
      <ModalOverlay />
      <ModalContent maxW="70%">
        <ModalHeader>{data?.name}</ModalHeader>
        <ModalCloseButton />
        <ModalBody as="form">
          <VStack spacing={2}>
            <Text my="10" whiteSpace="pre-line" padding="2">
              {data?.description}
            </Text>
            {data?.scripts?.map((script, index: number) => (
              <HStack w="100%" my="3" key={index} align="center">
                <Box w="2%"></Box>
                <Center
                  w="10%"
                  background="whiteAlpha.300"
                  boxSize="10"
                  fontSize="xl"
                  display="flex"
                  rounded="20"
                >
                  {index + 1}
                </Center>
                <Box w="2%"></Box>

                <Box
                  w="80%"
                  background="blackAlpha.900"
                  p="10"
                  rounded="10"
                  position="relative"
                >
                  <Text whiteSpace="pre-line">{script}</Text>
                  <IconButton
                    icon={<CopyIcon />}
                    aria-label="Copy"
                    size="xs"
                    color="white.100"
                    background="whiteAlpha.400"
                    position="absolute"
                    top="5"
                    right="5"
                    transform="translate(50%, -50%)" // 아이콘을 정확한 중앙으로 위치시킵니다.
                    onClick={() => copyToClipboard(script)} // 클릭 이벤트 핸들러를 추가합니다.
                  />
                </Box>
              </HStack>
            ))}
          </VStack>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
}
