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
  VStack,
  useToast,
} from "@chakra-ui/react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { FaUser, FaLock, FaEnvelope } from "react-icons/fa";
import { signUp } from "../api";

interface SignUpModalProps {
  isOpen: boolean;
  onClose: () => void;
}

interface ISignUp {
  username: string;
  email: string;
  password: string;
}

export default function SignUpModal({ isOpen, onClose }: SignUpModalProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<ISignUp>();

  const queryClient = useQueryClient();
  const toast = useToast();
  const mutation = useMutation(signUp, {
    onSuccess: () => {
      toast({
        status: "success",
        title: "Success SignUp!",
        position: "bottom-right",
      });
      onClose();
      reset();
    },
  });
  const onSubmit = ({ username, password, email }: ISignUp) => {
    mutation.mutate({ username, password, email });
  };
  return (
    <Modal onClose={onClose} isOpen={isOpen}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Sign up</ModalHeader>
        <ModalCloseButton />
        <ModalBody as="form" onSubmit={handleSubmit(onSubmit)}>
          <VStack>
            <InputGroup>
              <InputLeftElement
                children={
                  <Box color="gray.500">
                    <FaUser />
                  </Box>
                }
              />
              <Input
                variant={"filled"}
                placeholder="Username"
                {...register("username", {
                  required: "Please write a username",
                })}
              />
            </InputGroup>
            <InputGroup>
              <InputLeftElement
                children={
                  <Box color="gray.500">
                    <FaEnvelope />
                  </Box>
                }
              />
              <Input
                variant={"filled"}
                placeholder="Email"
                {...register("email", {
                  required: "Please write a email",
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
                placeholder="Password"
                type="password"
                {...register("password", {
                  required: "Please write a password",
                })}
              />
            </InputGroup>
          </VStack>
          <Button
            mt="10"
            mb="10"
            colorScheme="teal"
            w="100%"
            isLoading={mutation.isLoading}
            type="submit"
          >
            Sign Up
          </Button>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
}
