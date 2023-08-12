from rest_framework.views import APIView
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from django.contrib.auth import authenticate

from django.conf import settings
from . import serializers

import jwt


# Create your views here.
class SignUp(APIView):
    """회원가입 APIView"""

    def post(self, request):
        """회원가입 post 요청 처리

        Parameters:
            email (str) : 회원가입 email
            password (str) : 회원가입 password

        Raises:
            exceptions.ParseError: email,password 누락으로 회원가입 실패시 에러

        Returns:
            Response: 회원가입 완료 또는 실패 메세지
        """
        data = {
            "username": request.data.get("username"),
            "email": request.data.get("email"),
            "password": request.data.get("password"),
        }

        serializer = serializers.UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.UserSerializer(user)
            return Response({"message": "회원가입 완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"message": "회원가입 실패. 이미 존재하는 닉네임입니다. 또는 패스워드(8자 이상), 이메일 형식을 확인해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )
