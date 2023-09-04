import {
  Box,
  Center,
  Heading,
  HStack,
  Text,
  VStack,
  Image,
} from "@chakra-ui/react";

export default function TipPage() {
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
    <VStack p="20" align="flex-start" fontSize="lg" lineHeight="10">
      <Heading as="h1" fontSize="5xl" mb={4}>
        ChatGPT 질문 Tip
      </Heading>
      <Text mb={4} whiteSpace="pre-line" p="10">
        {
          "Chat GPT를 사용하기 전에 나의 질문을 받기 최적의 상태로 세팅하는 방식입니다.\n\
          여기서는 세팅이 아닌 질문 자체를 좀 더 잘하는 방법입니다.\n\n\
          Chat GPT가 없는 것을 만들어내거나 질문의 요점에 벗어나지 않고 성능을 잘 낼 수 있는 방식으로\n\
          'A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT' 이라는 논문에서 소개한 방식입니다.\n\n\
          \
          아래에서는 논문에서 제시한 다섯 가지 질문 패턴입니다. 이러한 패턴을 활용하여 \
          ChatGPT와의 상호작용을 향상시킬 수 있습니다."
        }
      </Text>

      {/* 페르소나 패턴 */}
      <Box mb={6}>
        <Heading as="h2" fontSize="3xl" mb={2}>
          The Persona pattern
        </Heading>
        <Text whiteSpace="pre-line" p="10" lineHeight="10">
          {
            '특정 인물이나 역할을 가정하고 질문에 답하는 방식입니다. 예를 들어,\n\n\
          "당신은 지금부터 짧은 퀴즈를 내는 교수 역할입니다. 내가 알려주는 자료에서 교수로서 학생들의 시험에 낼 만한 부분을\
           찾아 10개 내외로 퀴즈를 만들어주세요."\n\n\
          와 같은 방식으로 지정된 역할을 수행하여 답변합니다.\n\n\
          이런 역할을 부여할 때는 말투, 긍정적인 태도, 엄격한 판단 등의 요소를 부여할 수도 있습니다.'
          }
        </Text>
      </Box>

      {/* 레시피 패턴 */}
      <Box mb={6}>
        <Heading as="h2" fontSize="3xl" mb={2}>
          The Recipe Pattern
        </Heading>
        <Text whiteSpace="pre-line" p="10">
          {
            '단계별로 지시 사항을 따르는 방식으로 답변합니다. 예를 들어,\n\n\
            "지금부터 삼중 적분에 대한 수학 문제를 만들 것입니다. 문제는 반드시 상수 정답이 나오고,\
            식 뿐만 아니라 변수들끼리 관계를 알려주는 식이 나오고, 풀이도 같이 제시되고, 풀이는 최대한 자세하게 작성해야 합니다.\
             이것을 위해 수학 문제를 만들기 위해 필요한 순서와 과정을 알려주고, 추가적으로 필요한 단계를 확인해주세요"\n\n\
             와 같이 단계를 따라가며 설명합니다.\n\n\
             이는 말 그대로 내가 원하는 답변의 레시피를 제공하는 방식입니다.\n\
             이 방법의 장점은 내가 원하는 답변이 무엇인지 스스로 생각해볼수 있다는 점입니다. \
             스스로 어떤 답변을 원하는지 모르는 상태로 질문을 하면 질문할수록 늪에 빠지는 상황이 나올 수 있기 때문입니다.'
          }
        </Text>
      </Box>

      {/* 리플렉션 패턴 */}
      <Box mb={6}>
        <Heading as="h2" fontSize="3xl" mb={2}>
          The Reflection pattern
        </Heading>
        <Text whiteSpace="pre-line" p="10">
          {
            '모든 답변에 대한 이유를 설명하도록 ChatGPT에 요청하는 방식입니다. 예를 들어,\n\n\
          "내 질문에 답변을 할 때는 답변에 대한 근거와 가정을 설명하고 뒷받침하는 지식의 타당성을 설명합니다. \
          선택한 사항이 있다면 해당 사항에 대해 설명하며 잠재적인 제한 사항이나 엣지 케이스를 설명합니다."\n\n\
          이 방법은 특히 대학생에게 유용하다고 생각합니다. 전공 지식은 당연하고 전공이 아니더라도 이제 정보의 신뢰성에 대해 생각해야 하고\
           스스로 인터넷의 정보를 판단할 수 있는 능력을 키울 시점이니까요.\n\n\
           단순히 "Chat GPT답변 든든하다~" 하고 넘기기보단 어떤 방식으로 답변과 근거를 서술하고 전개해나가는지 배울 점이 많습니다!'
          }
        </Text>
      </Box>

      {/* 거부 차단기 패턴 */}
      <Box mb={6}>
        <Heading as="h2" fontSize="3xl" mb={2}>
          The Refusal Beraker Pattern
        </Heading>
        <Text whiteSpace="pre-line" p="10">
          {
            "ChatGPT가 일단 답변을 꺼내도록 하는 방법입니다. 예를 들어,\n\n\
          답변할 수 없을 때마다 그 이유를 자세히 설명해주세요. \
          그리고 이유를 피할 수 있는 대안을 반드시 하나 이상 제시하고 어떻게 대안이 나오게된 근거를 얘기합니다.\n\n\
          해당 방법은 다양한 의견이나 아이디어가 필요한 상황에서 사용할수록 좋습니다.\n\
          다만 공부를 하거나 어떤 명확한 정보가 필요한 상황에선 오히려 독이 될 가능성이 있습니다."
          }
        </Text>
      </Box>

      {/* 뒤집힌 상호작용 패턴 */}
      <Box mb={6}>
        <Heading as="h2" fontSize="3xl" mb={2}>
          The Flipped Interaction Pattern
        </Heading>
        <Text whiteSpace="pre-line" p="10">
          {
            'ChatGPT가 원하는 것을 달성할 때까지 역으로 질문하도록 하는 방식입니다.\n\
            쉽게 말하자면 Chat GPT가 나에게 스무고개 한다고 생각할 수 있습니다. 예를 들어, \n\n\
            "유명한 영화를 골라서 감상문을 2000자 내외로 작성해야 합니다. 이를 위해 필요한 질문을 나에게 하세요.\
            그리고 모든 정보를 얻으면 영화감상문을 작성해주세요."\n\n\
            와 같이 ChatGPT가 역으로 질문을 하며 필요한 정보를 얻습니다. 개인적으로 이 방법은 사용할수록 더 잘 이용할 수 있게 되는것 같습니다.'
          }
        </Text>
      </Box>
    </VStack>
  );
}
