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
} from "@chakra-ui/react";
import { FaEnvelope, FaLock } from "react-icons/fa";

interface RefBookModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function RefBookModal({ isOpen, onClose }: RefBookModalProps) {
  return (
    <Modal onClose={onClose} isOpen={isOpen}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Add Reference book</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <VStack>
            <InputGroup size={"md"}>
              <InputLeftElement
                children={
                  <Box color="gray.500">
                    <FaEnvelope />
                  </Box>
                }
              />
              <Input variant={"filled"} placeholder="제목" />
            </InputGroup>
            <InputGroup>
              <InputLeftElement
                children={
                  <Box color="gray.500">
                    <FaLock />
                  </Box>
                }
              />
              <Input variant={"filled"} placeholder="저자" />
            </InputGroup>
          </VStack>
          <Button mt={4} colorScheme={"red"} w="100%">
            추가하기
          </Button>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
}
