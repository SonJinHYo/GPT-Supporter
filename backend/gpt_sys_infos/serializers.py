from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import SystemInfo


class CreateSysInfoSerializer(ModelSerializer):
    class Meta:
        model = SystemInfo
        fields = (
            "description",
            "user",
            "language",
            "major",
            "understanding_level",
            "only_use_reference_data",
        )
