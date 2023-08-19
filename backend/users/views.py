from rest_framework.views import APIView
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

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


class SignIn(APIView):
    """jwt로그인 APIView"""

    def generate_token(self, user):
        """토큰 발행 함수

        Args:
            user (models.User): 인증된 유저 객체

        Returns:
            token (str): jwt토큰
        """
        payload = {"pk": user.pk}
        key = settings.SECRET_KEY
        token = jwt.encode(payload=payload, key=key, algorithm="HS256")
        return token

    def post(self, request):
        """jwt로그인 요청 처리 함수

        Parameters:
            email (str) : 로그인 email
            password (str) : 로그인 password

        Raises:
            exceptions.ParseError: email,password 누락으로 로그인 실패시 에러

        Returns:
            Response : jwt토큰 또는 오류 응답
        """

        username = request.data.get("email")
        password = request.data.get("password")

        if not username or not password:
            raise exceptions.ParseError()

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            token = self.generate_token(user)
            return Response({"token": token}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "유효하지 않은 닉네임과 패스워드 조합입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, reqest):
        user = reqest.user
        serializer = serializers.UserPrivateSerializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request):
        user = request.user
        serializer = serializers.UserPrivateSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
