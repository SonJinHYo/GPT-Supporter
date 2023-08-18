import {
  AddIcon,
  CloseIcon,
  QuestionIcon,
  SmallCloseIcon,
} from "@chakra-ui/icons";
import {
  Box,
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Heading,
  HStack,
  IconButton,
  SimpleGrid,
  Text,
  Tooltip,
  useDisclosure,
  VStack,
} from "@chakra-ui/react";
import { useState } from "react";
import { Link } from "react-router-dom";
import RefBookModal from "../components/RefbookModal";

interface IChatroom {
  pk: number;
  name: string;
  category: string;
  systemInformationDescription: string;
}

export default function Chatrooms() {
  const testData: IChatroom[] = [
    {
      pk: 1,
      name: "연첫단",
      category: "general",
      systemInformationDescription: "연애의첫단추 중간고사 자료",
    },
    {
      pk: 2,
      name: "수학2 계산",
      category: "eqution",
      systemInformationDescription: "",
    },
    {
      pk: 3,
      name: "36.5도 물리학",
      category: "general",
      systemInformationDescription: "중간고사까지 자료",
    },
  ];
  const [chatrooms, setCahtrooms] = useState<IChatroom[]>(testData);

  const removeBook = (pk: number) => {
    const updateChatrooms = chatrooms.filter((chatroom) => chatroom.pk !== pk);
    setCahtrooms(updateChatrooms);
  };

  const description: string =
    "ChatGPT와의 채팅방입니다. 설정된 system information이 적용되어 있습니다. 채팅방 카테고리에 따라 추가적인 질문이 가능하도록 세팅되어 있습니다.";
  const { isOpen: isOpen, onClose: onClose, onOpen: onOpen } = useDisclosure();
  return (
    <VStack align="flex-start" p="20">
      <HStack spacing="6">
        <Heading>Chat Rooms</Heading>
        <Tooltip label={description}>
          <IconButton aria-label={"heading"} icon={<QuestionIcon />} />
        </Tooltip>
      </HStack>
      <SimpleGrid
        w="80%"
        m={8}
        spacing={10}
        templateColumns="repeat(auto-fill, minmax(300px, 1fr))"
      >
        <IconButton
          w="100%"
          h="100%"
          aria-label={" "}
          icon={<AddIcon />}
          size="lg"
          onClick={onOpen}
        />
        {chatrooms?.map((chatroom) => (
          <Card key={chatroom.pk}>
            <CardHeader>
              <HStack justifyContent="space-between">
                <Heading size="md"> {chatroom.name}</Heading>
                <IconButton
                  aria-label="card-header"
                  icon={<SmallCloseIcon />}
                  size="s"
                  color="red.400"
                  onClick={() => removeBook(chatroom.pk)}
                />
              </HStack>
            </CardHeader>
            <CardBody>
              <Text>적용된 system information</Text>
              <Text mt="2">
                -{" "}
                {chatroom.systemInformationDescription !== ""
                  ? chatroom.systemInformationDescription
                  : " X "}
              </Text>
              <Text mt="4">Category : {chatroom.category}</Text>
            </CardBody>
            {/* <CardFooter>
                <Button onClick={() => handleOpenModal(audio)}> View Here</Button>
              </CardFooter> */}
          </Card>
        ))}
      </SimpleGrid>
      <RefBookModal isOpen={isOpen} onClose={onClose} />
    </VStack>
  );
}
