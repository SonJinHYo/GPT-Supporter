import { FaAirbnb, FaBook, FaFileAlt } from "react-icons/fa";
import { RiOpenaiFill } from "react-icons/ri";
import { BsChatLeft } from "react-icons/bs";
import {
  Box,
  Button,
  HStack,
  IconButton,
  Tooltip,
  useDisclosure,
} from "@chakra-ui/react";
import { Link } from "react-router-dom";
import LoginModal from "./LoginModal";
import SignUpModal from "./SIgnUpModal";

export default function Header() {
  const {
    isOpen: isLoginOpen,
    onClose: onLoginClose,
    onOpen: onLoginOpen,
  } = useDisclosure();
  const {
    isOpen: isSignUpOpen,
    onClose: onSignUpClose,
    onOpen: onSignUpOpen,
  } = useDisclosure();
  return (
    <HStack
      justifyContent={"space-between"}
      py={5}
      px={10}
      borderBottomWidth={1}
    >
      <Box color="red.500">
        <Link to={"/"}>
          <FaAirbnb size={"48"} />
        </Link>
      </Box>
      <HStack spacing="8">
        <Tooltip label="참고 서적">
          <Link to={"/books"}>
            <IconButton
              aria-label={"Ref-Books"}
              icon={<FaBook size="24" />}
              variant="ghost"
              alignSelf="flex-end"
            />
          </Link>
        </Tooltip>
        <Link to={"/data"}>
          <Tooltip label="참고 자료">
            <IconButton
              aria-label={"Ref-Data"}
              icon={<FaFileAlt size="24" />}
              variant="ghost"
              alignSelf="flex-end"
            />
          </Tooltip>
        </Link>
        <Link to={"/system-info"}>
          <Tooltip label="gpt 사전 설정">
            <IconButton
              aria-label={"system-info"}
              icon={<RiOpenaiFill size="24" />}
              variant="ghost"
              alignSelf="flex-end"
            />
          </Tooltip>
        </Link>
        <Tooltip label="채팅방">
          <IconButton
            aria-label={"Ref-Books"}
            icon={<BsChatLeft size="24" />}
            variant="ghost"
            alignSelf="flex-end"
          />
        </Tooltip>
      </HStack>
      <HStack spacing={2}>
        {/* <IconButton
          variant={"ghost"}
          aria-label="Toggle dark mode"
          icon={<FaMoon />}
        /> */}
        <Button onClick={onLoginOpen}>Log in</Button>
        <Button onClick={onSignUpOpen} colorScheme={"red"}>
          Sign up
        </Button>
      </HStack>
      <LoginModal isOpen={isLoginOpen} onClose={onLoginClose} />
      <SignUpModal isOpen={isSignUpOpen} onClose={onSignUpClose} />
    </HStack>
  );
}
