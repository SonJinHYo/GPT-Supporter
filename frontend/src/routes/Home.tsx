import { Box, Center, Heading, HStack, Text, VStack } from "@chakra-ui/react";

export default function Home() {
  const sequence = [
    "계정 생성, 로그인 후 상단의 책 버튼을 눌러 사용하는 책의 제목과 저자를 저장합니다. (로그인에 필요한 정보는 username, password입니다)",
    "책 버튼의 바로 옆에 있는 문서 버튼을 눌러 사용하는 텍스트 자료를 설정합니다. (ex. 강의에서 제공하는 자료)",
    "이어서 옆에 있는 ChatGPT 아이콘을 눌러 ChatGPT에게 전할 정보를 설정합니다.",
    "상세 설명은 각 페이지의 물음표 아이콘을 사용하시면 됩니다. 페이지별 부가 설명이 적혀있습니다!",
  ];
  return (
    <VStack spacing={10} fontSize="lg" w="100%" mb="100px">
      <Heading mt="20">GPT Supporter 사용방법</Heading>
      <Text fontSize="sm" color="whiteAlpha.700">
        GPT Supporter는 ChatGPT에게 질문하기 사용자의 데이터를 알려주는 템플릿을
        자동으로 생성해줍니다!.
      </Text>
      <VStack>
        <VStack justifyContent="flex-start" w="70%">
          {sequence?.map((text, index: number) => (
            <HStack w="100%" key={index} my="10">
              <Center
                w="10%"
                background="whiteAlpha.300"
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
          ))}
        </VStack>
      </VStack>
      {/* <VStack spacing={5}>
        <Text fontSize="xl">"ChatGPT는 거짓말을 한다."</Text>
        <Text fontSize="xl">"똑똑해 보이지만 막상 쓸모가..."</Text>
        <Text fontSize="xl">"가끔 진짜 멍청해. 똑같은 말만 반복한다니까?"</Text>
        <Text>.</Text>
        <Text>.</Text>
        <Text>.</Text>
        <Text>.</Text>
        <Text>.</Text>
        <Text>
          이런 문제가 발생하는 이유는 아마 기술적인 이유도 있겠지만 전달의
          방식이 문제될 가능성이 높습니다.
        </Text>
        <Text>
          상대방에게 내가 말하고자 하는 것을 전할 때 그리 어렵지 않습니다.
        </Text>
        <Text>
          하지만 100명, 1000명 이상의 사람에게 내 말을 오해없이 전달하려면
          상당히 어렵습니다.
        </Text>
        <Text>ChatGPT도 마찬가지입니다!</Text>
        <Text>
          수 많은 데이터가 있기에 우리에게 당연한 의도의 대화에서 다른 해석을 할
          수 있고
        </Text>
        <Text>
          수 많은 데이터가 있기에 원하는 대답 이외의 대답을 하게 됩니다.
        </Text>
        <Text>
          가끔 있지도 않은 정보를 거짓말로 답하는 것도 참조할 데이터가
          부족해서입니다!
        </Text>
      </VStack>
      <HStack>
        <VStack align="flex-start" my="20" w="50%" spacing={5}>
          <Text>
            ChatGPT는 우리와 대화를 해 나가며 우리의 패턴을 익히고 점점 우리에게
            만족스러운 대답을 할 수 있게 됩니다.
          </Text>
          <Text>
            쉽게 말해 GPT에게 '우리의 정보'를 알려줄수록 GPT는 우리에게 맞는
            대답을 할 수 있게 됩니다.
          </Text>
          <Text>
            내가 GPT에게 질문과 관련된 학과, 나의 이해도, 사용할 언어, 참고할
            자료, 전공 서적 등을 알려주고
          </Text>
          <Text>
            이 데이터를 참고해서 대답하라고 한다면 GPT는 훨씬 우리에게 잘 맞춰진
            방식으로 답을 할 것입니다.
          </Text>
          <Text>
            하지만 매번 하는 것도 귀찮고 ChatGPT의 해석이 매번 차이가 생길 수
            있습니다.
          </Text>
          <Text>
            그래서 우리는 ChatGPT가 오해하지 않도록 명확한 템플릿으로 전달해줘야
            합니다.
          </Text>
          <Text>
            ChatGPT 회사인 OpenAI의 ChatGPT 문서에서 확인할 수 있지만..
            그렇게까지 하면서 사용할 바엔 구글링하겠죠..?
          </Text>
        </VStack>
        <Box></Box>
      </HStack>

      <VStack>
        <Text>
          이제 GPT Supporter에서 사용할 데이터를 저장한 다음에 템플릿을 한 번에
          얻어가시면 됩니다!
        </Text>
        <Text>
          GPT Supporter는 사용자가 저장한 정보를 바탕으로 ChatGPT에게 사전에
          전할 스크립트를 자동 생성하여 전해줍니다.
        </Text>
      </VStack>
      <Text></Text>
      <Text></Text>
      <Text></Text> */}
    </VStack>
  );
}
