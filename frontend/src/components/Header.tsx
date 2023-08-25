import { FaHome, FaBook, FaFileAlt } from "react-icons/fa";
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
import { Link, useNavigate } from "react-router-dom";
import LoginModal from "./LoginModal";
import SignUpModal from "./SIgnUpModal";
import { useQueryClient } from "@tanstack/react-query";
import useUser from "../lib/userUser";

export default function Header() {
  const linkUrl = "https://chat.openai.com/";

  const { userLoading, isLoggedIn, user } = useUser();
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

  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const logout = () => {
    localStorage.removeItem("jwt"); // 토큰 삭제
    queryClient.clear(); // 캐시 클리어
  };

  return (
    <HStack
      justifyContent={"space-between"}
      py={5}
      px={10}
      borderBottomWidth={1}
    >
      <Box color="whiteAlpha.900" ml="10">
        <Link to={"/"}>
          <FaHome size={"48"} />
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
        {/* <Link to={"chatrooms"}> */}
        <Tooltip label="채팅방(미완)">
          <IconButton
            isDisabled
            aria-label={"Ref-Books"}
            icon={<BsChatLeft size="24" />}
            variant="ghost"
            alignSelf="flex-end"
          />
        </Tooltip>
        {/* </Link> */}
      </HStack>
      <HStack spacing={2}>
        {/* <IconButton
          variant={"ghost"}
          aria-label="Toggle dark mode"
          icon={<FaMoon />}
        /> */}
        {!userLoading ? (
          !isLoggedIn ? (
            <>
              <Button onClick={onLoginOpen}>Log in</Button>
              <Button onClick={onSignUpOpen} colorScheme={"red"} mr="10">
                Sign up
              </Button>
            </>
          ) : (
            <>
              <Tooltip label="ChatGPT 바로가기">
                <Button
                  onClick={() => {
                    window.open(linkUrl, "_blank");
                  }}
                >
                  Go ChatGPT
                </Button>
              </Tooltip>
              <Button
                mr="10"
                onClick={() => {
                  logout();
                  navigate("/"); // 페이지 새로고침
                }}
              >
                Log out
              </Button>
            </>
          )
        ) : null}
      </HStack>
      <LoginModal isOpen={isLoginOpen} onClose={onLoginClose} />
      <SignUpModal isOpen={isSignUpOpen} onClose={onSignUpClose} />
    </HStack>
  );
}
