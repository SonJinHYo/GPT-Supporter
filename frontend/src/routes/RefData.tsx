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
import { Link } from "react-router-dom";
import { deleteRefData, getRefData } from "../api";
import Loading from "../components/Loading";
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

  const [dataList, setDataList] = useState<IRefDataData[]>(testData);
  const { isLoading, data } = useQuery<IRefDataData[]>(
    ["ref-data"],
    getRefData
  );
  if (!isLoading && data && data !== dataList) {
    setDataList(data);
  }

  const mutation = useMutation(deleteRefData, {
    onSuccess: (dataList) => {
      window.location.reload();
    },
  });
  const handleRemoveData = (pk: number) => {
    mutation.mutate(pk); // deleteRefData 요청 실행
  };

  // const removeData = (pk: number) => {
  //   const updateData = data.filter((d) => d.pk !== pk);
  //   setData(updateData);
  // };
  const description: string =
    "ChatGPT에게 알려줄 자료 정보입니다. \
    저장된 자료는 GPT설정 페이지에서 선택하여 추가합니다.";
  const { isOpen: isOpen, onClose: onClose, onOpen: onOpen } = useDisclosure();
  return isLoading ? (
    <Loading />
  ) : (
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
        {dataList?.map((d) => (
          <Card key={d.pk}>
            <CardHeader>
              <HStack justifyContent="space-between">
                <Heading size="md"> {d.title}</Heading>
                <IconButton
                  aria-label="card-header"
                  icon={<SmallCloseIcon />}
                  size="s"
                  color="red.400"
                  onClick={() => {
                    handleRemoveData(d.pk);
                  }}
                />
              </HStack>
              <Text>{d.text}</Text>
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
