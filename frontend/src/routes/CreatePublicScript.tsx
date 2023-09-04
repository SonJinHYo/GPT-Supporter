import {
  Box,
  Button,
  Input,
  InputGroup,
  InputLeftElement,
  Textarea,
  VStack,
} from "@chakra-ui/react";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { createPublicScript } from "../api";
import { MdTitle } from "react-icons/md";
import { useState } from "react";

interface IPublicScriptVariables {
  name: string;
  description: string;
}

export default function CreatePublicScript() {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<IPublicScriptVariables>();

  const [scripts, setScripts] = useState<string[]>([]); // State로 scripts 배열을 관리합니다.

  const mutation = useMutation(createPublicScript, {
    onSuccess: () => {
      reset();
      window.location.reload();
    },
  });

  const onSubmit = ({ name, description }: IPublicScriptVariables) => {
    mutation.mutate({ name, description, scriptList: scripts });
  };

  const addScriptField = () => {
    // 텍스트 필드를 추가하기 위해 scripts 배열에 빈 문자열을 추가합니다.
    setScripts([...scripts, ""]);
  };

  const handleScriptChange = (index: number, value: string) => {
    // scripts 배열의 요소를 업데이트합니다.
    const updatedScripts = [...scripts];
    updatedScripts[index] = value;
    setScripts(updatedScripts);
  };

  const removeScriptField = (index: number) => {
    // 특정 인덱스의 텍스트 필드를 제거합니다.
    const updatedScripts = [...scripts];
    updatedScripts.splice(index, 1);
    setScripts(updatedScripts);
  };

  return (
    <VStack>
      <VStack
        w="80%"
        as="form"
        onSubmit={handleSubmit(onSubmit)}
        spacing="10"
        mt="20"
      >
        <InputGroup size={"md"}>
          <InputLeftElement
            children={
              <Box color="gray.500">
                <MdTitle />
              </Box>
            }
          />
          <Input
            variant={"filled"}
            placeholder="자료 제목"
            {...register("name", {
              required: "Please write a title",
            })}
          />
        </InputGroup>

        <Textarea
          variant={"filled"}
          placeholder="본문"
          h="400px"
          {...register("description", {
            required: "Please write a text",
          })}
        />
        {scripts.map((script, index) => (
          <InputGroup key={index} size="md">
            <Input
              variant="filled"
              placeholder={`Script #${index + 1}`}
              value={script}
              onChange={(e) => handleScriptChange(index, e.target.value)}
            />
            <Button
              colorScheme="red"
              size="sm"
              onClick={() => removeScriptField(index)}
            >
              Remove
            </Button>
          </InputGroup>
        ))}
        <Button my="2" colorScheme="blue" w="100%" onClick={addScriptField}>
          Add Script
        </Button>
        <Button
          my="10"
          colorScheme="teal"
          w="100%"
          isLoading={mutation.isLoading}
          type="submit"
        >
          추가하기
        </Button>
      </VStack>
    </VStack>
  );
}
