import {
  Text,
  Box,
  Button,
  Input,
  InputGroup,
  InputLeftElement,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalHeader,
  ModalOverlay,
  Textarea,
  useToast,
  VStack,
  Select,
} from "@chakra-ui/react";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { FaEnvelope, FaLock } from "react-icons/fa";
import { createChatroom, createRefData } from "../api";

interface ChatroomModalProps {
  isOpen: boolean;
  onClose: () => void;
  systemInfoPk: number;
}
interface IChatroom {
  name: string;
  category: string;
}

export default function ChatroomModal({
  isOpen,
  onClose,
  systemInfoPk,
}: ChatroomModalProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<IChatroom>();

  const mutation = useMutation(createChatroom, {
    onSuccess: () => {
      reset();
      window.location.reload();
    },
  });
  const onSubmit = ({ name, category }: IChatroom) => {
    mutation.mutate({ name, category, systemInfoPk });
  };
  return (
    <Modal onClose={onClose} isOpen={isOpen}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Add Reference Data</ModalHeader>
        <ModalCloseButton />
        <ModalBody as="form" onSubmit={handleSubmit(onSubmit)}>
          <VStack>
            <InputGroup size={"md"}>
              <InputLeftElement
                children={
                  <Box color="gray.500">
                    <FaEnvelope />
                  </Box>
                }
              />
              <Input
                variant={"filled"}
                placeholder="채팅방 이름"
                {...register("name", {
                  required: "Please write a title",
                })}
              />
            </InputGroup>
            <Select
              placeholder="GPT 사용 언어"
              {...register("category", {
                required: "Please choice a language",
              })}
            >
              <option value="general">일반 채팅</option>
              <option value="equation">수식 계산</option>
            </Select>
          </VStack>
          <Button
            mt={4}
            colorScheme={"red"}
            w="100%"
            isLoading={mutation.isLoading}
            type="submit"
          >
            추가하기
          </Button>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
}
