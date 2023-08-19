from time import sleep
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

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
                        raise exceptions.ParseError(f"참조 {related_model.__name__} 에러")

            return Response(status=status.HTTP_201_CREATED)


class SystemInfosList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = SystemInfo.objects.filter(user=request.user)
        pagination = PageNumberPagination()
        paginated_system_infos = pagination.paginate_queryset(
            queryset,
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
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

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
                            related_model.objects.get(pk=int(pk)) for pk in pk_list
                        ]
                        getattr(update_system_info, field_name.replace("_pk", "")).set(
                            related_objects
                        )
                    except:
                        raise exceptions.ParseError(f"참조 {related_model.__name__} 에러")
        return Response(
            serializers.SystemInfoDetailSerializer(update_system_info).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        system_info = self.get_object(pk)
        system_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateRefBook(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializers.CreateRefBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class RefBooksList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = RefBook.objects.filter(user=request.user)
        pagination = PageNumberPagination()
        paginated_ref_books = pagination.paginate_queryset(
            queryset,
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
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return RefBook.objects.get(pk=pk)
        except:
            raise exceptions.NotFound()

    def put(self, request, pk):
        ref_book = self.get_object(pk)
        serializer = serializers.CreateRefBookSerializer(
            ref_book,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        ref_book = self.get_object(pk)
        ref_book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateRefData(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ref_data_serializer = serializers.CreateRefDataSerializer(data=request.data)
        content_serializer = serializers.RefDataContentSerializer(data=request.data)

        if not ref_data_serializer.is_valid():
            return Response(
                ref_data_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not content_serializer.is_valid():
            return Response(
                content_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_ref_data = ref_data_serializer.save(user=request.user)
        content_serializer.save(data=new_ref_data)

        return Response(status=status.HTTP_201_CREATED)


class RefDatasList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = RefData.objects.filter(user=request.user)
        pagination = PageNumberPagination()
        paginated_ref_datas = pagination.paginate_queryset(
            queryset,
            request,
        )

        serializer = serializers.RefDataListSerializer(
            paginated_ref_datas,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class RefDataDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return RefData.objects.get(pk=pk)
        except:
            raise exceptions.NotFound()

    def put(self, request, pk):
        ref_data = self.get_object(pk)
        ref_data_serializer = serializers.RefDataListSerializer(
            ref_data,
            data=request.data,
            partial=True,
        )
        content_serializer = serializers.RefDataContentSerializer(
            ref_data.content,
            data=request.data,
            partial=True,
        )
        if not ref_data_serializer.is_valid():
            return Response(
                ref_data_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not content_serializer.is_valid():
            return Response(
                content_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        ref_data_serializer.save()
        content_serializer.save()

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        ref_data = self.get_object(pk)
        ref_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
