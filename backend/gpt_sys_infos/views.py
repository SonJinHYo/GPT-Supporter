from django.contrib.auth import authenticate

from rest_framework.views import APIView

from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import User

from .models import RefData, SystemInfo, RefBook

from . import serializers

import json


class CreateSystemInfo(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializers.CreateSystemInfoSerializer(data=request.data)
        if serializer.is_valid():
            new_system_info = serializer.save(user=request.user)
            if "ref_books_pk" in request.data:
                try:
                    books_pk_list = json.loads(request.data["ref_books_pk"])
                    ref_books = [RefBook.objects.get(pk=pk) for pk in books_pk_list]
                    new_system_info.ref_books.set(ref_books)
                except:
                    raise exceptions.ParseError()

            if "ref_datas_pk" in request.data:
                try:
                    data_pk_list = json.loads(request.data["ref_datas_pk"])
                    ref_datas = [RefData.objects.get(pk=pk) for pk in data_pk_list]
                    new_system_info.ref_datas.set(ref_datas)
                except:
                    raise exceptions.ParseError()

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SystemInfosList(APIView):
    permission_classes = [IsAuthenticated]
    queryset = SystemInfo.objects.all()

    def get(self, request):
        pagination = PageNumberPagination()
        paginated_system_infos = pagination.paginate_queryset(
            self.queryset,
            request,
        )

        serializer = serializers.ListSystemInfoSerializer(
            paginated_system_infos,
            many=True,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class SystemInfoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            system_info = SystemInfo.objects.get(pk=pk)
        except:
            raise exceptions.NotFound()

    def get(self, request, pk):
        system_info = self.get_object(pk)
        serializer = serializers.SystemInfoDetailSerializer(system_info)
        return Response(
            system_info.data,
            status=status.HTTP_200_OK,
        )
