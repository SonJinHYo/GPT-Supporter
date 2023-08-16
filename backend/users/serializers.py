from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import User


class UserSerializer(ModelSerializer):
    # 회원가입, 로그인 시 사용

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )

    def create(self, validated_data):
        # 암호화

        password = validated_data.pop("password", None)
        new_user = self.Meta.model(**validated_data)

        if password is not None:
            new_user.set_password(password)
        new_user.save()

        return new_user


class UserPrivateSerializer(ModelSerializer):
    chat_room_name_list = SerializerMethodField()
    sys_info_description_list = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "using_token",
            "chat_room_name_list",
            "sys_info_description_list",
            "created_at",
            "updated_at",
        )

    def get_chat_room_name_list(self, user_obj):
        return [chatroom.name for chatroom in user_obj.chatrooms.all()]

    def get_sys_info_description_list(self, user_obj):
        return [system_info.description for system_info in user_obj.system_infos.all()]
