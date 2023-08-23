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
  useToast,
  VStack,
} from "@chakra-ui/react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { Link } from "react-router-dom";
import { deleteRefBook, getRefBooks } from "../api";
import Loading from "../components/Loading";
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
  // const [deleteBookPk, setDeleteBookPk] = useState<number>(-1);
  const [books, setBooks] = useState<IRefBookData[]>(testBooks);
  const { isLoading, data } = useQuery<IRefBookData[]>(
    ["ref-books"],
    getRefBooks
  );
  if (!isLoading && data && books !== data) {
    setBooks(data);
  }

  const mutation = useMutation(deleteRefBook, {
    onSuccess: (data) => {
      window.location.reload();
    },
  });
  const handleRemoveBook = (pk: number) => {
    mutation.mutate(pk); // deleteRefBook 요청 실행
  };

  // const removeBook = (pk: number) => {
  //   const updateBooks = books.filter((book) => book.pk !== pk);
  //   setBooks(updateBooks);
  // };

  const description: string =
    "참고 서적 목록입니다. 이곳에 저장된 책 정보는 ChatGPT에게 알려줄 참고 서적으로 선택할 수 있습니다.";
  const { isOpen: isOpen, onClose: onClose, onOpen: onOpen } = useDisclosure();
  return isLoading ? (
    <Loading />
  ) : (
    <VStack align="flex-start" p="20">
      <HStack spacing="6">
        <Heading>Reference Books</Heading>
        <Tooltip label={description}>
          <IconButton aria-label={"heading"} icon={<QuestionIcon />} />
        </Tooltip>
      </HStack>
      <Text>
        ChatGPT는 영어 기반 데이터를 가지고 있기 때문에 원문 서적, 영문 책을
        권장합니다.
      </Text>
      <Text color="whiteAlpha.700" fontSize="sm">
        한국어로 이루어진 책도 불가능하지 않습니다!
      </Text>
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
                  onClick={() => {
                    handleRemoveBook(book.pk);
                  }}
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
