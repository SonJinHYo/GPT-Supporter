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

interface IRefBookData {
  pk: number;
  author: string;
  title: string;
}

export default function RefBooks() {
  const testBooks: IRefBookData[] = [
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
  const [books, setBooks] = useState<IRefBookData[]>(testBooks);

  const removeBook = (pk: number) => {
    const updateBooks = books.filter((book) => book.pk !== pk);
    setBooks(updateBooks);
  };

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
        {books?.map((book) => (
          <Card key={book.pk}>
            <CardHeader>
              <HStack justifyContent="space-between">
                <Heading size="md"> {book.title}</Heading>
                <IconButton
                  aria-label="card-header"
                  icon={<SmallCloseIcon />}
                  size="s"
                  color="red.400"
                  onClick={() => removeBook(book.pk)}
                />
              </HStack>
              <Text>{book.author}</Text>
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