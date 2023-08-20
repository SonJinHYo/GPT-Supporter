import {} from "@chakra-ui/icons";
import { Box, Button, Input, Text, Textarea, VStack } from "@chakra-ui/react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import ReactMarkdown from "react-markdown";

interface IChatroom {
  pk: number;
  name: string;
  category: string;
  system_info_description: string;
}

export default function WebSocketChat() {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [messages, setMessages] = useState<string[]>([]);
  const [messageInput, setMessageInput] = useState("");
  const { chatroomPk } = useParams();

  // const testData = [
  //   "자 간다?",
  //   "네, 질문이 있다면 언제든지 제가 준비되어 있습니다. 무엇을 도와드릴까요?",
  //   "너는 아는게 뭐야?",
  //   "저는 여러 분야의 지식을 가지고 있습니다. 주로 과학, 엔지니어링, 수학, 역사 등에 대해 알고 있습니다. 물리학에 대해서도 상세한 지식을 갖고 있습니다. 어떤 주제에 대해 궁금하신가요? 물리학 관련 질문이 있다면 언제든지 물어보세요!",
  //   "물리학보다 대단한 학과가 있어?",
  //   "물리학은 매우 흥미로운 학문 분야 중 하나입니다. 하지만 어떤 학과가 '대단하다'라고 정확히 말하기는 어렵습니다. 모든 학과와 분야는 각자의 고유한 가치와 중요성을 가지고 있습니다. 예를 들어, 수학, 화학, 생물학, 컴퓨터 과학 등은 물리학과 마찬가지로 중요하고 세련된 학문 분야입니다. 각각의 분야는 문제 해결에 기여하고 사회에 영향을 미칠 수 있는 방법과 도구를 제공합니다. 따라서 물리학은 흥미로운 학문 분야 중 하나이며, 다른 학문 분야와 연계하여 현실 세계의 복잡한 문제를 이해하고 해결하는 데 도움이 될 수 있습니다.",
  //   "아니 물리학이 가장 대단한 학과야 오키?",
  //   '네, 물리학은 매우 중요하고 흥미로운 학문 분야 중 하나입니다. 물리학은 자연과학의 기초를 다루며 우리 주변에서 일어나는 현상을 이해하고 설명하는 역할을 합니다. 물리학은 우주의 기원과 동작, 물질의 구성과 상호작용, 에너지의 변환 등 다양한 분야에 대한 깊은 이해를 제공합니다. 이를 통해 우리가 주변에서 경험하는 사건들을 예측하고 기술적인 혁신과 과학적 발전에 기여할 수 있습니다. 그러나 각각의 학문 분야는 그 자체로 독특하고 중요한 가치를 가지고 있으며, 각자의 고유한 기여를 하고 있습니다. 따라서 어떤 학과가 "대단하다"라고 말하기보다는, 다양한 학문 분야가 상호보완적으로 연결돼 인류의 지식과 발전에 기여하고 있다고 말할 수 있습니다.',
  //   "아니 가장 대단해",
  //   '물리학은 확실히 매우 중요하고 근본적인 학문 분야 중 하나입니다. 물리학의 기본 원리와 이론들은 우리가 주변에서 경험하는 현상을 이해하고 예측하는 데에 매우 유용합니다. 또한 물리학은 기술과 과학의 발전에도 핵심적인 역할을 담당하고 있습니다. 그러나 "가장 대단한 학과"를 결정하는 것은 개인의 선호와 관점에 따라 다를 수 있습니다. 다른 학문 분야들도 서로 다른 방식으로 사회와 자연을 이해하고 발전시키는데 기여하고 있으며, 중요한 역할을 하고 있습니다. 따라서, 물리학은 대단한 학문 분야 중 하나이지만, 다른 학문 분야들과의 상호보완적인 관계를 감안할 때, 절대적으로 "가장 대단한" 학과라고 단정하기는 어렵습니다.',
  //   "아니 절대적으로 가장 대단해",
  //   '저는 여러 학문 분야가 모두 독특하고 중요한 가치를 가지고 있다고 믿습니다. 모든 학문 분야는 다양한 방식으로 사회와 자연을 이해하고 발전시키는 데에 기여하고 있습니다. 각각의 분야는 자신만의 독특한 관점과 기술을 제공하며, 사회를 위한 혁신과 발전을 이끌어내는 역할을 합니다. 물리학은 물론이고, 수학, 화학, 생물학, 공학, 의학, 사회과학 등 다양한 학문 분야들이 모두 중요하고 대단한 분야라고 할 수 있습니다. 이러한 다양한 분야들이 함께 상호작용하고 협력하여 인류의 지식과 발전을 이끌어내는 것이 중요한 것입니다. 따라서 모든 학문 분야가 뛰어나다고 말할 수 있지만, 절대적으로 "가장 대단한" 학문 분야를 정하거나 비교하는 것은 어렵습니다.',
  //   "[ B_n(x) = sum_{k=0}^{n} \binom{n}{k} b_k x^{n-k} ]. 이 식은 뭐야?",
  // ];

  useEffect(() => {
    const token: any = localStorage.getItem("jwt");
    const newSocket = new WebSocket(
      `ws://127.0.0.1:8000/api/v1/chatrooms/${chatroomPk}?${token}`
    );
    console.log(chatroomPk);
    newSocket.onopen = () => {
      console.log("WebSocket connection established");
    };

    newSocket.onmessage = (event) => {
      const newMessage = JSON.parse(event.data);
      const GPTMessage = newMessage.message;
      //   const GPTMessage = newMessage.message.replace(
      //   /[-/\\^$*+?.()|[\]{}]/g,
      //   "\\$&"
      // );
      setMessages((prevMessages) => [...prevMessages, GPTMessage]);
      console.log(GPTMessage);
    };

    newSocket.onclose = () => {
      console.log("WebSocket connection closed");
    };

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  const sendMessage = () => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      const myMessage: any = JSON.stringify({ message: messageInput });
      socket.send(myMessage);
      console.log(myMessage);
      setMessages([...messages, messageInput]);

      setMessageInput("");
    }
  };

  return (
    <VStack p={4}>
      <Text fontSize="xl" mb={4}>
        WebSocket Chat Example
      </Text>
      {/* {testData.map((message, index) => ( */}
      {messages.map((message, index) => (
        <Box
          p={4}
          background={index % 2 === 0 ? "gray.700" : "gray.900"}
          maxHeight="300px"
          overflowY="scroll"
          key={index}
          w="70%"
        >
          <ReactMarkdown>{message}</ReactMarkdown>
        </Box>
      ))}
      <Textarea
        value={messageInput}
        onChange={(e) => setMessageInput(e.target.value)}
        placeholder="Type your message..."
        mt={4}
      />
      <Button onClick={sendMessage} mt={2} colorScheme="blue">
        {/* <Button mt={2} colorScheme="blue"> */}
        Send
      </Button>
    </VStack>
  );
}
