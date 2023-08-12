from rest_framework.views import APIView
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

from django.conf import settings

from . import serializers


class CreateSysInfo(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializers.CreateSysInfoSerializer(request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_201_CREATED)
