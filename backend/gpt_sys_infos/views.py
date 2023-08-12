from django.contrib.auth import authenticate

from rest_framework.views import APIView

from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import User

from gpt_sys_infos.models import SystemInfo

from . import serializers


class CreateSysInfo(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializers.SysInfoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SysInfosList(APIView):
    permission_classes = [IsAuthenticated]
    queryset = SystemInfo.objects.all()

    def get(self, request):
        pagination = PageNumberPagination()
        paginated_system_infos = pagination.paginate_queryset(
            self.queryset,
            request,
        )

        serializer = serializers.ListSysInfoSerializer(
            paginated_system_infos,
            many=True,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
