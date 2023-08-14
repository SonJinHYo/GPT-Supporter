from django.contrib.auth import authenticate
from django.db import transaction
from django.conf import settings

from rest_framework.views import APIView

from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import ChatRoom
from users.models import User


from . import serializers

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
        chatrooms = ChatRoom.objects.all()
        serializer = serializers.CreateChatRoomSerializer(
            chatrooms,
            many=True,
        )
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
