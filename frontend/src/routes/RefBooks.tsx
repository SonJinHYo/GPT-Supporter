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
import RefBookModal from "../components/RefbookModal";

interface IRefBookData {
  pk: number;
  author: string;
  title: string;
}

export default function RefBooks() {
  const testData: IRefBookData[] = [
    {
      pk: 1,
      author: "책 저자1",
      title: "책 제목1",
    },
    {
      pk: 2,
      author: "책 저자2",
      title: "책 제목2",
    },
    {
      pk: 3,
      author: "책 저자3",
      title: "책 제목3",
    },
  ];
  const description: string =
    "ChatGPT에게 사용하고 있는 책 정보를 알려줍니다. 저장된 책은 GPT설정 페이지에서 선택하여 추가합니다.";
  const { isOpen: isOpen, onClose: onClose, onOpen: onOpen } = useDisclosure();
  return (
    <VStack align="flex-start" p="20">
      <HStack spacing="6">
        <Heading>Reference Books</Heading>
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
              <Text>{data.author}</Text>
            </CardHeader>
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
