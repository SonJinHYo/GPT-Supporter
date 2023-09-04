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


class PublicScriptDetail(ModelSerializer):
    scripts = SerializerMethodField()

    class Meta:
        model = PublicScript
        fields = (
            "pk",
            "name",
            "description",
            "scripts",
        )

    def get_scripts(self, obj: PublicScript) -> list:
        return [script.text for script in obj.scripts.all().order_by("number")]


class PublicScriptsListSerializer(ModelSerializer):
    description_summary = SerializerMethodField()

    class Meta:
        model = PublicScript
        fields = (
            "pk",
            "name",
            "description_summary",
        )

    def get_description_summary(self, obj: PublicScript) -> list:
        return (
            obj.description
            if len(obj.description) < 400
            else obj.description[:400] + "..."
        )
