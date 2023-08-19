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
} from "@chakra-ui/react";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { FaEnvelope, FaLock } from "react-icons/fa";
import { createRefData } from "../api";

interface RefDataModalProps {
  isOpen: boolean;
  onClose: () => void;
}
interface IRefData {
  title: string;
  text: string;
}

export default function RefDataModal({ isOpen, onClose }: RefDataModalProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<IRefData>();

  const mutation = useMutation(createRefData, {
    onSuccess: () => {
      reset();
      window.location.reload();
    },
  });
  const onSubmit = ({ title, text }: IRefData) => {
    mutation.mutate({ title, text });
  };
  return (
    <Modal onClose={onClose} isOpen={isOpen}>
      <ModalOverlay />
      <ModalContent maxW="70%">
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
                placeholder="자료 제목"
                {...register("title", {
                  required: "Please write a title",
                })}
              />
            </InputGroup>
            <Textarea
              variant={"filled"}
              placeholder="본문"
              h="400px"
              {...register("text", {
                required: "Please write a text",
              })}
            />
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
