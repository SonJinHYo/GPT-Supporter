import { AddIcon, QuestionIcon, SmallCloseIcon } from "@chakra-ui/icons";
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
import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { deleteSystemInfo, getSystemInfo } from "../api";
import ChatroomModal from "../components/ChatroomModal";
import Loading from "../components/Loading";
import SystemInfoModal from "../components/SystemInfoModal";

interface ISystemInfoData {
  pk: number;
  description: string;
  user: number;
  language: string;
  major: string;
  understanding_level: number;
  only_use_reference_data: boolean;
  data_sequence: boolean;
  ref_book_title: string;
  ref_data_title: string;
}

export default function SystemInfo() {
  const nav = useNavigate();
  const testData: ISystemInfoData[] = [
    {
      pk: 1,
      description: "36.5도 물리학 자료",
      user: 1,
      language: "ko",
      major: "Physics",
      understanding_level: 2,
      only_use_reference_data: false,
      data_sequence: false,
      ref_book_title: "책 제목",
      ref_data_title: "참조 데이xj 제목222222",
    },
    {
      pk: 2,
      description: "연애의첫단추 중간고사 자료",
      user: 1,
      language: "ko",
      major: "Psychology",
      understanding_level: 1,
      only_use_reference_data: false,
      data_sequence: true,
      ref_book_title: "책 제목",
      ref_data_title:
        "참조 데이터 제목3 참조 데이터 제목3참조 데이터 제목3참조 데이터 제목3참조 데이터 제목3참조 데이터 제목3",
    },
    {
      pk: 1,
      description: "미시경제 자료 설정",
      user: 1,
      language: "ko",
      major: "Economics",
      understanding_level: 4,
      only_use_reference_data: false,
      data_sequence: false,
      ref_book_title: "책 제목, 책 제목 2",
      ref_data_title: "",
    },
  ];

  const [systemInfos, setSystemInfos] = useState<ISystemInfoData[]>(testData);
  const [systemInfoPk, setSystemInfoPk] = useState<number>(-1);
  const { isLoading, data } = useQuery<ISystemInfoData[]>(
    ["system-info"],
    getSystemInfo
  );
  if (!isLoading && data && data !== systemInfos) {
    setSystemInfos(data);
  }

  const mutation = useMutation(deleteSystemInfo, {
    onSuccess: (data) => {
      window.location.reload();
    },
  });

  const handleRemoveData = (pk: number) => {
    mutation.mutate(pk); // deleteRefData 요청 실행
  };

  const description: string =
    "ChatGPT 채팅을 시작하기 전에 ChatGPT에게 전달할 정보입니다. \
    생성 후 Get Scripts를 누르면 GPT 채팅을 시작하기 전에 전할 스크립트를 제공합니다. ";
  const { isOpen: isOpen, onClose: onClose, onOpen: onOpen } = useDisclosure();
  const {
    isOpen: isChatroomOpen,
    onClose: onChatroomClose,
    onOpen: onChatroomOpen,
  } = useDisclosure();
  return isLoading ? (
    <Loading />
  ) : (
    <VStack align="flex-start" p="20" w="100%">
      <HStack spacing="6">
        <Heading>System Information</Heading>
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
        {systemInfos?.map((data) => (
          <Card key={data.pk}>
            <CardHeader>
              <HStack justifyContent="space-between">
                <Heading size="md"> {data.description}</Heading>
                <IconButton
                  aria-label="card-header"
                  icon={<SmallCloseIcon />}
                  size="s"
                  color="red.400"
                  onClick={() => handleRemoveData(data.pk)}
                />
              </HStack>
            </CardHeader>
            <CardBody overflow="auto">
              <Text>
                GPT사용 언어: {data.language === "ko" ? "Korean" : "English"}
              </Text>
              <Text mt="3">관련 전공: {data.major}</Text>
              <Text mt="3">
                답변 수준(대학 기준): {data.understanding_level}학년
              </Text>
              <Text mt="3">참조 책 정보 : {data.ref_book_title}</Text>
              <Text mt="3">참조 자료 정보 : {data.ref_data_title}</Text>
              <Text mt="3">
                참조 데이터 위주 답변 :
                {data.only_use_reference_data ? "O" : "X"}
              </Text>
              <Text>참조 자료 순서 유무: {data.data_sequence ? "O" : "X"}</Text>
            </CardBody>
            <CardFooter>
              {/* <Button
                onClick={() => {
                  setSystemInfoPk(data.pk);
                  onChatroomOpen();
                }}
              >
                Create Chatroom
              </Button> */}
              <Button
                onClick={() => {
                  nav(`/system-info/${data.pk}/dialogues`);
                }}
              >
                Get Scripts
              </Button>
            </CardFooter>
          </Card>
        ))}
      </SimpleGrid>
      <SystemInfoModal isOpen={isOpen} onClose={onClose} />
      <ChatroomModal
        isOpen={isChatroomOpen}
        onClose={onChatroomClose}
        systemInfoPk={systemInfoPk}
      />
    </VStack>
  );
}
