import { AddIcon, QuestionIcon } from "@chakra-ui/icons";
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
import { Link } from "react-router-dom";
import SystemInfoModal from "../components/SystemInfoModal";

interface SystemInfoData {
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
  const testData: SystemInfoData[] = [
    {
      pk: 1,
      description: "시스템 설정 설명 수정",
      user: 1,
      language: "ko",
      major: "물리학과",
      understanding_level: 2,
      only_use_reference_data: false,
      data_sequence: false,
      ref_book_title: "책 제목",
      ref_data_title: "참조 데이xj 제목222222",
    },
    {
      pk: 2,
      description: "시스템 설정 설명 수정",
      user: 1,
      language: "ko",
      major: "물리학과",
      understanding_level: 4,
      only_use_reference_data: false,
      data_sequence: true,
      ref_book_title: "책 제목",
      ref_data_title:
        "참조 데이터 제목3 참조 데이터 제목3참조 데이터 제목3참조 데이터 제목3참조 데이터 제목3참조 데이터 제목3",
    },
    {
      pk: 1,
      description: "시스템 설정 설명 수정",
      user: 1,
      language: "ko",
      major: "물리학과",
      understanding_level: 2,
      only_use_reference_data: false,
      data_sequence: false,
      ref_book_title: "책 제목, 책 제목 2",
      ref_data_title: "",
    },
  ];
  const description: string =
    "ChatGPT 채팅을 시작하기 전에 ChatGPT에게 전달할 정보입니다. \
    시작된 채팅은 제공된 System Information을 기본값으로 시작됩니다. ";
  const { isOpen: isOpen, onClose: onClose, onOpen: onOpen } = useDisclosure();
  return (
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
        {testData?.map((data) => (
          <Card key={data.pk}>
            <CardHeader>
              <Heading size="md"> {data.description}</Heading>
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
              {/* <Text>
                {audio.modified_script.length > 100
                  ? `${audio.modified_script.slice(0, 97)}...`
                  : audio.modified_script}
              </Text> */}
            </CardBody>
          </Card>
        ))}
      </SimpleGrid>
      <SystemInfoModal isOpen={isOpen} onClose={onClose} />
    </VStack>
  );
}
