import {
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
  useToast,
  VStack,
} from "@chakra-ui/react";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { FaEnvelope, FaLock } from "react-icons/fa";
import { createRefBook } from "../api";

interface RefBookModalProps {
  isOpen: boolean;
  onClose: () => void;
}
interface IRefBook {
  author: string;
  title: string;
}

export default function RefBookModal({ isOpen, onClose }: RefBookModalProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<IRefBook>();

  const toast = useToast();
  const mutation = useMutation(createRefBook, {
    onSuccess: () => {
      reset();
      window.location.reload();
    },
  });
  const onSubmit = ({ author, title }: IRefBook) => {
    mutation.mutate({ author, title });
  };
  return (
    <Modal onClose={onClose} isOpen={isOpen}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Add Reference book</ModalHeader>
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
                placeholder="제목"
                {...register("title", {
                  required: "Please write a title",
                })}
              />
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
                placeholder="저자"
                {...register("author", {
                  required: "Please write a author",
                })}
              />
            </InputGroup>
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
