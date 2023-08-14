from django.contrib.auth import authenticate
from django.db import transaction
from django.conf import settings

from rest_framework.views import APIView

from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import ChatRoom, Message
from users.models import User


from . import serializers
from .chatapi import post_chat_api

import json


class CreateChatRoom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = User.objects.get(pk=request.user.pk)

        if user.chatrooms.cout() > settings.CHATROOMS_MAX_SIZE:
            return Response(
                {"message": "채팅방은 최대 10개까지 개설이 가능합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = serializers.CreateChatRoomSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user)

        return Response(status=status.HTTP_201_CREATED)


class ChatRoomsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chatrooms = ChatRoom.objects.filter(user=request.user).order_by("-updated_at")
        serializer = serializers.ChatRoomsListSerializer(
            chatrooms,
            many=True,
        )
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatRoomsDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ChatRoom.objects.get(pk=pk)
        except:
            raise exceptions.NotFound("채팅방 데이터를 찾을 수 없습니다.")

    def get(self, request, pk):
        chatroom = self.get_object(pk)
        serializer = serializers.ChatRoomDetailSerializer(chatroom)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
