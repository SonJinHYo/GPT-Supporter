from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Content, RefBook, RefData, SystemInfo


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


class SystemInfoListSerializer(ModelSerializer):
    ref_book_title = SerializerMethodField()
    ref_data_title = SerializerMethodField()

    class Meta:
        model = SystemInfo
        fields = (
            "pk",
            "description",
            "user",
            "language",
            "major",
            "understanding_level",
            "only_use_reference_data",
            "data_sequence",
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


class SystemInfoDetailSerializer(ModelSerializer):
    ref_books = SerializerMethodField()
    ref_datas = SerializerMethodField()

    class Meta:
        model = SystemInfo
        fields = (
            "pk",
            "description",
            "user",
            "language",
            "major",
            "understanding_level",
            "only_use_reference_data",
            "data_sequence",
            "ref_books",
            "ref_datas",
        )

    def get_ref_books(self, system_info_obj):
        books = system_info_obj.ref_books.all()
        books_list = []

        for book in books:
            data = {
                "author": book.author,
                "title": book.title,
            }
            books_list.append(data)

        return books_list

    def get_ref_datas(self, system_info_obj):
        datas = system_info_obj.ref_datas.all()
        data_list = []

        for data in datas:
            text = data.content.text
            data = {"title": data.title, "text": text}
            data_list.append(data)

        return data_list


class CreateRefBookSerializer(ModelSerializer):
    class Meta:
        model = RefBook
        fields = (
            "author",
            "title",
        )


class RefBookListSerializer(ModelSerializer):
    class Meta:
        model = RefBook
        fields = (
            "pk",
            "author",
            "title",
        )


class CreateRefDataSerializer(ModelSerializer):
    class Meta:
        model = RefData
        fields = ("title",)


class RefDataContentSerializer(ModelSerializer):
    class Meta:
        model = Content
        fields = ("text",)


class RefDataListSerializer(ModelSerializer):
    text = SerializerMethodField()

    class Meta:
        model = RefData
        fields = (
            "pk",
            "title",
            "text",
        )

    def get_text(self, ref_data_object):
        return ref_data_object.content.text
