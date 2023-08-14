from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import ChatRoom


class CreateChatRoomSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = (
            "name",
            "category",
        )
