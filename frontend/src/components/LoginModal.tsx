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
  useQuery,
  useToast,
  VStack,
} from "@chakra-ui/react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { FaEnvelope, FaLock } from "react-icons/fa";
import { signIn } from "../api";

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
}
interface IForm {
  username: string;
  password: string;
}
export default function LoginModal({ isOpen, onClose }: LoginModalProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<IForm>();
  const toast = useToast();

  const queryClient = useQueryClient();
  const mutation = useMutation(signIn, {
    onSuccess: () => {
      toast({
        status: "success",
        title: "Success Login",
        position: "bottom-right",
      });
      queryClient.refetchQueries(["me"]);
      onClose();
      reset();
    },
  });
  const onSubmit = ({ username, password }: IForm) => {
    mutation.mutate({ username, password });
  };

  return (
    <Modal onClose={onClose} isOpen={isOpen}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Log in</ModalHeader>
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
                placeholder="username"
                {...register("username", {
                  required: "Please write a username",
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
            mt={4}
            colorScheme={"red"}
            w="100%"
            isLoading={mutation.isLoading}
            type="submit"
          >
            Log in
          </Button>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
}
