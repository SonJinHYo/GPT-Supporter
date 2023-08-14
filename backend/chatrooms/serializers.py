from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import ChatRoom, Message


class CreateChatRoomSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = (
            "name",
            "category",
        )


class SendMessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ("text",)
