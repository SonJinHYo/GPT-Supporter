from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import PublicScript, Script


class CreatePublicScriptSerializer(ModelSerializer):
    class Meta:
        model = PublicScript
        fields = (
            "name",
            "description",
        )


class CreateScriptSerializer(ModelSerializer):
    class Meta:
        model = Script
        fields = (
            "number",
            "text",
        )
