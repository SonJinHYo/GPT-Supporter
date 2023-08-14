from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import ChatRoom, Message


class CreateChatRoomSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = (
            "name",
            "category",
        )


class ChatRoomsListSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = (
            "pk",
            "name",
            "category",
        )


class ChatRoomDetailSerializer(ModelSerializer):
    messages = SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ("name", "category", "messages")

    def get_messages(self, chatroom_obj):
        return [
            message.text
            for message in chatroom_obj.messages.all().order_by("created_at")
        ]


class SendMessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ("text",)
