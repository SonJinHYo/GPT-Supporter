from django.contrib import admin
from .models import *


@admin.register(PublicScript)
class PublicScriptAdmin(admin.ModelAdmin):
    """PublicScript 관리"""

    list_display = (
        "name",
        "summary",
    )

    def summary(self, obj: PublicScript):
        return obj.description[:20] + "..." if obj.description > 20 else obj.description


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    """Script 관리"""

    list_display = ("fk_and_number",)

    def fk_and_number(self, obj: Script):
        return f"{obj.public_script.name} - {obj.number} 스크립트"
