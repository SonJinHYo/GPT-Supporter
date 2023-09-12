import {
  Box,
  Center,
  Heading,
  HStack,
  Text,
  VStack,
  Image,
} from "@chakra-ui/react";

export default function Home() {
  const sequence = [
    "계정 생성, 로그인 후 상단의 책 버튼을 눌러 사용하는 책의 제목과 저자를 저장합니다. (로그인에 필요한 정보는 username, password입니다)",
    "책 버튼의 바로 옆에 있는 문서 버튼을 눌러 사용하는 텍스트 자료를 설정합니다. (ex. 강의에서 제공하는 자료)",
    "이어서 옆에 있는 ChatGPT 아이콘을 눌러 ChatGPT에게 전할 정보를 설정합니다.",
    "추가가 완료되면 마찬가지로 설정된 정보를 담은 카드가 생성됩니다. 'Get Scripts'를 누르면 템플릿이 생성됩니다.",
  ];
  const last_sequence = [
    "스크립트가 생성된 모습입니다! ChatGPT로 이동해서 순서대로 대화를 붙여넣으면 됩니다.",
    "ChatGPT는 같은 말을 다르게 해석하는 경우도 있습니다. 좋을 때도 있고 나쁠 때도 있습니다. 지금은 일관성있게 초기 설정을 전달해야하니 번역의 실수가 없도록 영어로 전달을 합니다.",
    "갑자기 한글이 나와도 괜찮고, ChatGPT가 중간에 의도하지 않은 말을 해도 괜찮습니다. ChatGPT는 대화 목록 전체를 참고하기 때문에 설정이 이어지면서 교정이 될 수 있습니다.",
    "마지막까지 전하고나서 채팅을 시작하면 됩니다! ChatGPT에게 추가적인 설정을 원한다면 생성된 템플릿에 원하는대로 덧붙여 설정하면 됩니다.",
  ];
  return (
    <VStack spacing={10} fontSize="lg" w="100%" mb="100px">
      <Heading mt="20">GPT Supporter 사용방법</Heading>
      <Text fontSize="md" color="whiteAlpha.700">
        GPT Supporter는 ChatGPT에게 질문하기 전에 사용자의 데이터를 알려주는
        템플릿을 자동으로 생성해줍니다.
      </Text>
      <Text fontSize="md" color="whiteAlpha.700">
        사용방법은 대략적인 가이드라인이며 각 페이지별로 부가적인 설명이
        있습니다!
      </Text>
      <VStack>
        <VStack justifyContent="flex-start" w="70%">
          {sequence?.map((text, index: number) => (
            <VStack my="20">
              <HStack w="100%" key={index} my="10">
                <Center
                  w="10%"
                  background="teal"
                  boxSize="14"
                  fontSize="2xl"
                  display="flex"
                  rounded="28"
                >
                  {index + 1}
                </Center>
                <Box w="5%"></Box>
                <Box
                  w="80%"
                  background="blackAlpha.900"
                  p="10"
                  rounded="10"
                  position="relative"
                >
                  <Text>{text}</Text>
                </Box>
              </HStack>
              <Image
                p="0.5"
                bg="whiteAlpha.900"
                src={`/images/my-gpt-${index + 1}.png`}
              />
            </VStack>
          ))}
          {last_sequence?.map((text, index: number) => (
            <VStack my="20">
              <HStack w="100%" key={index} my="10">
                <Center
                  w="10%"
                  background="teal"
                  boxSize="14"
                  fontSize="2xl"
                  display="flex"
                  rounded="28"
                >
                  {index + 5}
                </Center>
                <Box w="5%"></Box>
                <Box
                  w="80%"
                  background="blackAlpha.900"
                  p="10"
                  rounded="10"
                  position="relative"
                >
                  <Text>{text}</Text>
                </Box>
              </HStack>
              <Image
                p="0.5"
                bg="whiteAlpha.900"
                src={`/images/my-gpt-5-${index + 1}.png`}
              />
            </VStack>
          ))}
        </VStack>
      </VStack>
    </VStack>
  );
}
