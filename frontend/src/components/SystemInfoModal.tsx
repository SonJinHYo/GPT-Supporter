import {
  Text,
  Box,
  Button,
  HStack,
  Input,
  InputGroup,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalHeader,
  ModalOverlay,
  VStack,
  Select,
  useToast,
  Textarea,
  Checkbox,
  Grid,
  GridItem,
} from "@chakra-ui/react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { createSystemInfo, getRefBooks, getRefData } from "../api";
import Loading from "./Loading";

interface SystemInfoModalProps {
  isOpen: boolean;
  onClose: () => void;
}
interface IRefDataData {
  pk: number;
  title: string;
  text: string;
}
interface IRefBookData {
  pk: number;
  author: string;
  title: string;
}
interface ISystemInfo {
  description: string;
  language: string;
  major: string;
  understanding_level: number;
  only_use_reference_data: boolean;
  data_sequence: boolean;
  ref_books_pk: number[];
  ref_datas_pk: number[];
}

export default function SystemInfoModal({
  isOpen,
  onClose,
}: SystemInfoModalProps) {
  const testRefBooks: IRefBookData[] = [
    {
      pk: 1,
      author: "책 저자1",
      title: "책 제목1",
    },
    {
      pk: 2,
      author: "책 저자2",
      title: "책 제목2",
    },
    {
      pk: 3,
      author: "책 저자3",
      title: "책 제목3",
    },
  ];
  const testRefData: IRefDataData[] = [
    {
      pk: 1,
      title: "자료 제목",
      text: "본문",
    },
    {
      pk: 2,
      title: "자료 제목2",
      text: "본문",
    },
    {
      pk: 3,
      title: "자료 제목3",
      text: "본문",
    },
  ];
  const { isLoading: isRefDataLoading, data: refData } = useQuery<
    IRefDataData[]
  >(["ref-data"], getRefData);
  const { isLoading: isRefBooksLoading, data: refBooks } = useQuery<
    IRefBookData[]
  >(["ref-books"], getRefBooks);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<ISystemInfo>();

  const toast = useToast();
  const [refBooksPk, setRefBooksPk] = useState<number[]>([]);
  const [refDataPk, setRefDataPk] = useState<number[]>([]);
  const [onlyUseRefData, setOnlyUseRefData] = useState<boolean>(false);
  const [dataSequence, setDataSequence] = useState<boolean>(false);
  const mutation = useMutation(createSystemInfo, {
    onSuccess: () => {
      reset();
      window.location.reload();
    },
  });
  const onSubmit = ({
    description,
    language,
    major,
    understanding_level,
  }: ISystemInfo) => {
    mutation.mutate({
      description,
      language,
      major,
      understanding_level,
      data_sequence: dataSequence,
      only_use_reference_data: onlyUseRefData,
      ref_books_pk: refBooksPk,
      ref_datas_pk: refDataPk,
    });
  };

  return isRefBooksLoading && isRefBooksLoading ? (
    <Loading />
  ) : (
    <Modal onClose={onClose} isOpen={isOpen}>
      <ModalOverlay />
      <ModalContent maxW="70%">
        <ModalHeader>Add System Information</ModalHeader>
        <ModalCloseButton />
        <ModalBody as="form" onSubmit={handleSubmit(onSubmit)}>
          <VStack>
            <Text fontSize="2xl" fontStyle="italic">
              Tip
            </Text>
            <VStack
              justifyContent="start"
              w="70%"
              align="flex-start"
              spacing="5"
              mt="4"
              mb="8"
            >
              <Text>
                * 시스템 설정 설명은 GPT에게 전할 내용이 아닌 사용자가 알아보기
                쉽도록 간단히 설명을 달아놓는 부분입니다.
              </Text>
              <Box>
                <Text>
                  * 관련 전공은 본인의 전공이 아닌 GPT에게 질문할 전공입니다.
                </Text>
                <Text color="gray.400" fontSize="sm">
                  (영어 권장 ex - Physics, Electrical engineering)
                </Text>
              </Box>
              <Text>
                * 석사 수준의 대답을 받길 원한다면 답변 수준에 '5'를
                입력해주세요. 석사 수준은 참고 자료를 적용하고 것을 권장하고,
                박사 이상의 수준은 ChatGPT 이외의 수단을 권장합니다.
              </Text>
            </VStack>
            <Textarea
              variant={"filled"}
              placeholder="시스템 설정 설명"
              {...register("description", {
                required: "Please write a description",
              })}
            />
            <Select
              placeholder="GPT 사용 언어"
              {...register("language", {
                required: "Please choice a language",
              })}
            >
              <option value="ko">한국어</option>
              <option value="en">English</option>
            </Select>
            <InputGroup>
              <Input
                variant={"filled"}
                placeholder="관련 전공"
                {...register("major", {
                  required: "Please write a major",
                })}
              />
            </InputGroup>
            <InputGroup>
              <Input
                variant={"filled"}
                placeholder="답변 수준           (대학 학년 기준 [1 ~ 5])"
                {...register("understanding_level", {
                  required: "Please write a understanding_level",
                })}
              />
            </InputGroup>
            <Grid
              templateRows="repeat(2,1fr)"
              templateColumns="repeat(5,1fr)"
              gap={5}
              rounded={5}
              backgroundColor="gray.900"
              p={3}
              w="100%"
            >
              <GridItem rowSpan={2} colSpan={1}>
                참조 서적
              </GridItem>
              {refBooks?.map((book) => (
                <Checkbox
                  colorScheme="green"
                  key={book.pk}
                  isChecked={refBooksPk.includes(book.pk)} // 체크 여부 확인
                  onChange={(e) => {
                    if (e.target.checked) {
                      // 체크되었을 때 해당 pk를 배열에 추가
                      setRefBooksPk((prevPk) => [...prevPk, book.pk]);
                      console.log(refBooksPk);
                    } else {
                      // 체크 해제되었을 때 해당 pk를 배열에서 제거
                      setRefBooksPk((prevPk) =>
                        prevPk.filter((pk) => pk !== book.pk)
                      );
                      console.log(refBooksPk);
                    }
                  }}
                >
                  {book.title}
                </Checkbox>
              ))}
            </Grid>
            <Grid
              templateRows="repeat(2,1fr)"
              templateColumns="repeat(5,1fr)"
              gap={5}
              rounded={5}
              backgroundColor="gray.900"
              p={3}
              w="100%"
            >
              <GridItem rowSpan={2} colSpan={1}>
                참조 자료
              </GridItem>
              {refData?.map((data) => (
                <GridItem colSpan={1} key={data.pk}>
                  <Checkbox
                    colorScheme="green"
                    isChecked={refDataPk.includes(data.pk)} // 체크 여부 확인
                    onChange={(e) => {
                      if (e.target.checked) {
                        // 체크되었을 때 해당 pk를 배열에 추가
                        setRefDataPk((prevPk) => [...prevPk, data.pk]);
                      } else {
                        // 체크 해제되었을 때 해당 pk를 배열에서 제거
                        setRefDataPk((prevPk) =>
                          prevPk.filter((pk) => pk !== data.pk)
                        );
                      }
                    }}
                  >
                    {data.title}
                    {refDataPk.indexOf(data.pk) !== -1
                      ? " (" + (refDataPk.indexOf(data.pk) + 1) + "번)"
                      : null}
                  </Checkbox>
                </GridItem>
              ))}
            </Grid>
            <HStack
              justifyContent="flex-start"
              w="100%"
              background="gray.900"
              p={3}
              rounded={5}
            >
              <HStack>
                <Text>참조자료 순서 적용하기</Text>
                {refDataPk.length < 2 ? (
                  <Checkbox isDisabled></Checkbox>
                ) : (
                  <Checkbox
                    colorScheme="green"
                    isChecked={dataSequence}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setDataSequence(true);
                      } else {
                        setDataSequence(false);
                      }
                    }}
                  />
                )}
              </HStack>
              <HStack ml="12">
                <Text>참조자료 위주 답변 받기</Text>
                {refDataPk.length === 0 ? (
                  <Checkbox isDisabled></Checkbox>
                ) : (
                  <Checkbox
                    colorScheme="green"
                    isChecked={onlyUseRefData}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setOnlyUseRefData(true);
                      } else {
                        setOnlyUseRefData(false);
                      }
                    }}
                  />
                )}
              </HStack>
            </HStack>
          </VStack>
          <Button
            mt="20"
            mb="10"
            colorScheme="teal"
            w="100%"
            isLoading={mutation.isLoading}
            type="submit"
          >
            추가하기
          </Button>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
}
