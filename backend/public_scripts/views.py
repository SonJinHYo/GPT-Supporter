from rest_framework.views import APIView
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response

from django.db import transaction

from .models import PublicScript

from . import serializers


class CreatePublicScript(APIView):
    """관리자만 생성 가능한 공용 스크립트 생성 APIVIew"""

    def post(self, request):
        if request.user.is_superuser is False:
            return Response(
                {"message": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        public_script_serializer = serializers.CreatePublicScriptSerializer(
            data=request.data
        )

        script_list = request.data["scriptList"]

        if not public_script_serializer.is_valid():
            raise exceptions.ParseError("공용 스크립트 생성 실패. 스크립트 이름 및 설명을 확인하세요.")

        try:
            with transaction.atomic():
                new_public_script_serializer = public_script_serializer.save(
                    user=request.user
                )

                for script in script_list:
                    script_serializer = serializers.CreateScriptSerializer(data=script)
                    if not script_serializer.is_valid():
                        return Response(
                            script_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    script_serializer.save(
                        public_script=new_public_script_serializer,
                    )
                return Response(status=status.HTTP_201_CREATED)

        except:
            transaction.rollback()
            return Response(
                {"message": "서버 문제로 공용 스크립트 생성에 실패했습니다"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PublicScriptList(APIView):
    """공용 스크립트 리스트 APIView"""

    def get(self, request):
        serializer = serializers.PublicScriptsListSerializer(
            PublicScript.objects.all(),
            many=True,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class PublicScriptDetail(APIView):
    def get_object(self, pk):
        try:
            return PublicScript.objects.get(pk=pk)
        except:
            return exceptions.NotFound("존재하지 않는 PublicScript 객체입니다.")

    def get(self, request, pk):
        public_script = self.get_object(pk)
        serializer = serializers.PublicScriptDetailSerializer(public_script)
        return Response(serializer.data, status=status.HTTP_200_OK)
