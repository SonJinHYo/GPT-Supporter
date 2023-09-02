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


class PublicScriptsListSerializer(ModelSerializer):
    scripts = SerializerMethodField()

    class Meta:
        model = PublicScript
        fields = (
            "name",
            "description",
            "scripts",
        )

    def get_scripts(self, obj: PublicScript) -> list:
        return [script.text for script in obj.scripts.all().order_by("number")]
