from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import SystemInfo


class CreateSystemInfoSerializer(ModelSerializer):
    class Meta:
        model = SystemInfo
        fields = (
            "description",
            "language",
            "major",
            "understanding_level",
            "only_use_reference_data",
        )


class ListSystemInfoSerializer(ModelSerializer):
    ref_book_title = SerializerMethodField()
    ref_data_title = SerializerMethodField()

    class Meta:
        model = SystemInfo
        fields = (
            "description",
            "user",
            "language",
            "major",
            "understanding_level",
            "only_use_reference_data",
            "ref_book_title",
            "ref_data_title",
        )

    def get_ref_book_title(self, system_info_obj):
        return ", ".join(
            [ref_book.title for ref_book in system_info_obj.ref_books.all()]
        )

    def get_ref_data_title(self, system_info_obj):
        return ", ".join(
            [ref_data.title for ref_data in system_info_obj.ref_datas.all()]
        )
