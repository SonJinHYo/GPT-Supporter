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
    system_info_description = SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = (
            "pk",
            "name",
            "category",
            "system_info_description",
        )

    def get_system_info_description(self, chatroom_obj):
        return chatroom_obj.system_info.description


class ChatRoomDetailSerializer(ModelSerializer):
    messages = SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ("name", "category", "messages")
        ordering = ["updateed_at"]

    def get_messages(self, chatroom_obj):
        return [
            message.text
            for message in chatroom_obj.messages.all().order_by("created_at")
        ]


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "role",
            "content",
        )
        ordering = ["created_at"]
