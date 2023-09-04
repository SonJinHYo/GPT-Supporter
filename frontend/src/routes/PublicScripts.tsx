import { AddIcon, QuestionIcon, SmallCloseIcon } from "@chakra-ui/icons";
import {
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
import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getPublicScripts } from "../api";
import Loading from "../components/Loading";
import PublicScriptModal from "../components/PublicScriptModal";

interface IPublicScriptVariables {
  pk: number;
  name: string;
  description_summary: string;
}

export default function PublicScripts() {
  const nav = useNavigate();

  const { isLoading, data, isError, error } = useQuery<
    IPublicScriptVariables[]
  >(["public-scripts"], getPublicScripts);

  if (isError && (error as any)?.response.status === 403) {
    console.log(error);
    nav("/forbidden");
  }

  const description: string =
    "공용 스크립트 목록입니다. 필요한 스크립트를 찾아보고 사용해보세요!";
  const { isOpen: isOpen, onClose: onClose, onOpen: onOpen } = useDisclosure();

  return isLoading ? (
    <Loading />
  ) : (
    <VStack align="flex-start" p="20" w="100%">
      <HStack spacing="6">
        <Heading>Public Scripts</Heading>
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
        {data?.map((publicScript) => (
          <Card key={publicScript.name}>
            <CardHeader>
              <HStack justifyContent="space-between">
                <Heading size="md"> {publicScript.name}</Heading>
              </HStack>
              <CardBody maxH="50%">
                <Text whiteSpace="pre-line">
                  {publicScript.description_summary}
                </Text>
              </CardBody>
            </CardHeader>
            <CardFooter>
              <Button onClick={onOpen}> View Here</Button>
            </CardFooter>
            <PublicScriptModal
              isOpen={isOpen}
              onClose={onClose}
              publicScriptPk={publicScript.pk}
            />
          </Card>
        ))}
      </SimpleGrid>
    </VStack>
  );
}
