import codecs
import json
import os
import pprint
import openai
from io import StringIO


from channels.generic.websocket import JsonWebsocketConsumer

from django.contrib.auth import authenticate
from django.db import transaction
from django.conf import settings
from django.utils import encoding
from rest_framework.views import APIView

from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from gpt_sys_infos.models import SystemInfo

from .models import ChatRoom, Message
from users.models import User
from . import serializers
from config.authentication import ws_authenticate
from gpt_sys_infos.serializers import SystemInfoDetailSerializer


class CreateChatRoom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = User.objects.get(pk=request.user.pk)

        if user.chatrooms.count() > settings.CHATROOMS_MAX_SIZE:
            return Response(
                {"message": "채팅방은 최대 10개까지 개설이 가능합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = serializers.CreateChatRoomSerializer(data=request.data)
        print(request.data.get("system_info_pk"))
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer.save(
                user=request.user,
                system_info=SystemInfo.objects.get(
                    pk=request.data.get("system_info_pk")
                ),
            )
        except:
            raise exceptions.NotFound("Not found system info pk")

        return Response(status=status.HTTP_201_CREATED)


class ChatRoomsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chatrooms = ChatRoom.objects.filter(user=request.user).order_by("-updated_at")
        serializer = serializers.ChatRoomsListSerializer(
            chatrooms,
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatRoomsDetail(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_messages = []
        self.stream_messages = []
        self.user = None
        self.chatroom = None

    def connect(self):
        self.chatroom = self.get_chatroom()
        if self.chatroom is None:
            self.close()

        else:
            system_info = self.chatroom.system_info
            serializer = SystemInfoDetailSerializer(system_info)

            self.set_pre_messages(
                system_info=serializer.data, category=self.chatroom.category
            )
            print("채팅방 설정 완료...")

            # if self.chatroom.messages.exists():
            #     message_serializer = serializers.MessageSerializer(
            #         self.chatroom.messages.all(),
            #         many=True,
            #     )

            #     self.stream_messages = message_serializer.data
            print("메세지 설정 완료...")

            self.accept()

    def disconnect(self, code):
        for message in self.stream_messages:
            Message.objects.create(
                chatroom=self.chatroom,
                role=message["role"],
                content=message["content"],
            )
        return super().disconnect(code)

    def receive_json(self, content, **kwargs):
        if "rm_message" in content:  # 삭제(해당 메세지 수정) 키워드가 들어오면
            reset_messages_index = int(content["rm_message"])  # 해당 키워드에서 메세지의 인덱스를 파악하고
            if 0 <= reset_messages_index < len(self.stream_messages):  # 유효한 인덱스라면
                self.stream_messages = (  # 해당 메세지'까지' 삭제. 이후 해당 메세지 부분을 전송받은대로 재장
                    self.stream_messages[: reset_messages_index + 1]
                )

        user_message = content["message"]
        self.stream_messages.append({"role": "user", "content": user_message})
        pprint.pprint(self.set_messages + self.stream_messages)
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.set_messages + self.stream_messages,
            )
        except:
            raise exceptions.server_error("openai api 통신 실패")

        self.user.using_token += completion["usage"]["total_tokens"]
        self.user.save()
        print(completion)
        response_content = completion["choices"][0]["message"]["content"]
        print(response_content)
        self.stream_messages.append({"role": "assistant", "content": response_content})

        self.send_json({"message": response_content})

    def get_chatroom(self):
        self.user, _ = ws_authenticate(self.scope)
        print(self.scope)
        chatroom_pk = self.scope["url_route"]["kwargs"]["chatroom_pk"]
        try:
            return ChatRoom.objects.get(pk=chatroom_pk)
        except ChatRoom.DoesNotExist:
            return None

    def set_pre_messages(self, system_info, category):
        language = "Korean" if system_info["language"] == "ko" else "English"
        major = system_info["major"]
        understanding_level = system_info["understanding_level"]
        only_use_reference_data = system_info["only_use_reference_data"]
        ref_books = system_info["ref_books"]
        ref_datas = system_info["ref_datas"]
        data_sequence = system_info["data_sequence"]
        openai.api_key = os.environ.get("OPENAI_KEY")

        ########     System role Set     ########
        system_role_content = f"You are asked questions about {major}.I want you to answer according to the level of the {understanding_level} year of college.And respond in {language}, whether the user is using English or Korean."

        self.set_messages.append(
            {
                "role": "system",
                "content": system_role_content,
            },
        )

        ########     User role Set     ########

        if ref_books:
            ref_books_string = ""
            for ref_book in ref_books:
                ref_books_string += f"'{ref_book['author']} - {ref_book['title']}', "

            user_role_book_content = f"I will now provide you with the titles and authors of the books the I'm using. I will state them in the format of 'Author - Title'. {ref_books_string[:-2]}. The information about my books concludes here."
            self.set_messages.append(
                {
                    "role": "user",
                    "content": user_role_book_content,
                },
            )
            self.set_messages.append(
                {
                    "role": "user",
                    "content": "my books information ",
                },
            )
        if ref_datas:
            user_role_data_content = 'I have reference materials. Each piece of material is enclosed within three double quotation marks in the following format:"""title: , content: """. Please keep this format in mind when responding.'
            if data_sequence:
                user_role_data_content += " Also, the data I provide to you will have an order following the sequence I inform you of."

            if only_use_reference_data:
                user_role_data_content += " Please prioritize responses based on the reference materials I've sent for now."
                self.set_messages.append(
                    {
                        "role": "user",
                        "content": user_role_data_content,
                    }
                )

            for i, ref_data in enumerate(ref_datas, start=1):
                self.set_messages.append(
                    {
                        "role": "user",
                        "content": f'material {i}. """title: {ref_data["title"]}, content: {ref_data["text"]}"""',
                    }
                )
            self.set_messages.append(
                {
                    "role": "user",
                    "content": f"The information about my reference materials concludes here.",
                }
            )
        if category == "eqution":
            self.set_messages.append(
                {
                    "role": "user",
                    "content": "you will receive math equations with Korean mixed in. When asking for a math equation, I will enclose it with three backticks. Then, show the corresponding equation in expressed as LaTeX code.You should send the LaTeX code enclosed in a Math Block format. If there are any typos in the interpreted equation or mathematically incorrect expressions, please let me know it's incorrect and provide the reasons.",
                }
            )

        self.set_messages.append(
            {
                "role": "user",
                "content": "I've provided all the information. I will now begin asking questions. Please keep information in mind when responding.",
            }
        )


class SendMessage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):  # pk : chatroom의 pk
        text = request.data.get("text")
        chatroom = ChatRoom.objects.get(pk=pk)
        serializer = serializers.SendMessageSerializer(data={"text": text})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(
            sender=request.user.username,
            chatroom=chatroom,
        )

        # try:
        #     chat_api_response = post_chat_api(text)
        # except:
        #     return Response(
        #         {"message": "ChatGPT에게 요청이 실패했습니다."},
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     )
        # chat_api_message = chat_api_response["message"]

        ################################################################
        #########            테스트용 데이터                  ###########
        ################################################################
        chat_api_message = "테스트 메세지"  ###########
        ################################################################

        chat_api_seralizer = serializers.SendMessageSerializer(
            data={"text": chat_api_message}
        )

        if chat_api_seralizer.is_valid():
            return Response(
                {"message": "올바른 답변을 받지 못했습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        chat_api_seralizer.save(
            sender="gpt",
            chatroom=chatroom,
        )

        return Response({"message": chat_api_message}, status=status.HTTP_200_OK)
