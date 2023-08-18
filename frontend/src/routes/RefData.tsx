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
import RefDataModal from "../components/RefDataModal";

interface IRefDataData {
  pk: number;
  title: string;
  text: string;
}

export default function RefDatas() {
  const testData: IRefDataData[] = [
    {
      pk: 1,
      title: "자료 제목",
      text: "본문",
    },
    {
      pk: 2,
      title: "자료 제목2",
      text: "본문",
    },
    {
      pk: 3,
      title: "자료 제목3",
      text: "본문",
    },
  ];
  const description: string =
    "ChatGPT에게 알려줄 자료 정보입니다. \
    저장된 자료는 GPT설정 페이지에서 선택하여 추가합니다.";
  const { isOpen: isOpen, onClose: onClose, onOpen: onOpen } = useDisclosure();
  return (
    <VStack align="flex-start" p="20">
      <HStack spacing="6">
        <Heading>Reference Data</Heading>
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
              <Heading size="md"> {data.title}</Heading>
              <Text>{data.text}</Text>
            </CardHeader>
            {/* <CardFooter>
              <Button onClick={() => handleOpenModal(audio)}> View Here</Button>
            </CardFooter> */}
          </Card>
        ))}
      </SimpleGrid>
      <RefDataModal isOpen={isOpen} onClose={onClose} />
    </VStack>
  );
}
