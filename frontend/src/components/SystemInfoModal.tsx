import {
  Text,
  Box,
  Button,
  HStack,
  Input,
  InputGroup,
  InputLeftElement,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalHeader,
  ModalOverlay,
  Radio,
  RadioGroup,
  Stack,
  VStack,
  Select,
} from "@chakra-ui/react";
import { useState } from "react";
import { FaEnvelope, FaLock } from "react-icons/fa";

interface SystemInfoModalProps {
  isOpen: boolean;
  onClose: () => void;
}
interface IRefDataData {
  pk: number;
  title: string;
  text: string;
}
interface IRefBookData {
  pk: number;
  author: string;
  title: string;
}
export default function SystemInfoModal({
  isOpen,
  onClose,
}: SystemInfoModalProps) {
  const testRefBooks: IRefBookData[] = [
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
  const testRefData: IRefDataData[] = [
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
  return (
    <Modal onClose={onClose} isOpen={isOpen}>
      <ModalOverlay />
      <ModalContent maxW="70%">
        <ModalHeader>Add System Information</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <VStack>
            <VStack>
              <Text>
                * 관련 전공은 본인의 전공이 아닌 GPT에게 질문할 전공입니다.
              </Text>
              <Text>(영어 권장 ex. Physics, Electrical engineering)</Text>
            </VStack>
            <Select placeholder="GPT 사용 언어">
              <option value="ko">한국어</option>
              <option value="en">English</option>
            </Select>

            <InputGroup>
              <InputLeftElement
                children={
                  <Box color="gray.500">
                    <FaLock />
                  </Box>
                }
              />
              <Input variant={"filled"} placeholder="관련 전공" />
            </InputGroup>
            <InputGroup>
              <InputLeftElement
                children={
                  <Box color="gray.500">
                    <FaLock />
                  </Box>
                }
              />
              <Input
                variant={"filled"}
                placeholder="답변 수준(대학 학년 기준)"
              />
            </InputGroup>

            <Select placeholder="GPT 참조 서적">
              {testRefBooks?.map((data) => (
                <option value={data.title}>{data.title}</option>
              ))}
            </Select>
            <Select placeholder="GPT 참조 자료">
              {testRefData?.map((data) => (
                <option value={data.title}>{data.title}</option>
              ))}
            </Select>
          </VStack>
          <Button mt={4} colorScheme={"red"} w="100%">
            추가하기
          </Button>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
}
