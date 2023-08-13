from django.contrib.auth import authenticate
from django.db import transaction

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
            with transaction.atomic():
                new_system_info = serializer.save(user=request.user)
                for field_name in ["ref_books_pk", "ref_datas_pk"]:
                    if field_name in request.data:
                        try:
                            pk_list = json.loads(request.data[field_name])
                            related_model = (
                                RefBook if field_name == "ref_books_pk" else RefData
                            )
                            related_objects = [
                                related_model.objects.get(pk=pk) for pk in pk_list
                            ]
                            getattr(new_system_info, field_name.replace("_pk", "")).set(
                                related_objects
                            )
                        except:
                            raise exceptions.ParseError(
                                f"참조 {related_model.__name__} 에러"
                            )

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

        serializer = serializers.SystemInfoListSerializer(
            paginated_system_infos,
            many=True,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class SystemInfoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            system_info = SystemInfo.objects.get(pk=pk)
            return system_info
        except:
            raise exceptions.NotFound()

    def get(self, request, pk):
        system_info = self.get_object(pk)
        serializer = serializers.SystemInfoDetailSerializer(system_info)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        system_info = self.get_object(pk)

        serializer = serializers.CreateSystemInfoSerializer(
            system_info,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            with transaction.atomic():
                update_system_info = serializer.save()
                for field_name in ["ref_books_pk", "ref_datas_pk"]:
                    if field_name in request.data:
                        try:
                            pk_list = json.loads(request.data[field_name])
                            related_model = (
                                RefBook if field_name == "ref_books_pk" else RefData
                            )
                            related_objects = [
                                related_model.objects.get(pk=pk) for pk in pk_list
                            ]
                            getattr(
                                update_system_info, field_name.replace("_pk", "")
                            ).set(related_objects)
                        except:
                            raise exceptions.ParseError(
                                f"참조 {related_model.__name__} 에러"
                            )
            return Response(
                update_system_info.data,
                status=status.HTTP_200_OK,
            )
        else:
            return update_system_info.errors

    def delete(self, request, pk):
        system_info = self.get_object(pk)
        system_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateRefBook(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializers.CreateRefBookSerializer(data=request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_201_CREATED)
        else:
            return serializer.errors


class RefBooksList(APIView):
    permission_classes = [IsAuthenticated]
    queryset = RefBook.objects.all()

    def get(self, request):
        pagination = PageNumberPagination()
        paginated_ref_books = pagination.paginate_queryset(
            self.queryset,
            request,
        )

        serializer = serializers.RefBookListSerializer(
            paginated_ref_books,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class RefBookDetail(APIView):
    def get_object(self, pk):
        try:
            return RefBook.objects.get(pk=pk)
        except:
            raise exceptions.NotFound()

    def put(self, request, pk):
        ref_book = self.get_object(pk)
        serializer = serializers.RefBookListSerializer(
            ref_book,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return serializer.errors

    def delete(self, request, pk):
        ref_book = self.get_object(pk)
        ref_book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
