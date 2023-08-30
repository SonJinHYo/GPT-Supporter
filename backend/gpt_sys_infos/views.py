from django.db import transaction

from rest_framework.views import APIView

from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import RefData, SystemInfo, RefBook


from . import serializers

import json


class CreateSystemInfo(APIView):
    """SystemInfo 생성 APIView"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """SystemInfo 생성 요청 함수

        Parameters:
            serializer (dict) : key값 - description, language, major, understanding_level, only_use_reference_data
            new_system_info (.models.SystemInfo) : 새롭게 생성된 SystemInfo 객체
            related_model : RefBook 또는 RefData 모델
            related_objects (list) : RefBook 또는 RefData 객체 리스트

        Raises:
            exceptions.ParseError: ref_books 또는 ref_datas 의 pk가 존재하지 않는 경우

        Returns:
            Response : SystemInfo 생성 처리상태 반환
        """

        # 요청받은 데이터를 직렬화
        serializer = serializers.CreateSystemInfoSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # save이후 추가 데이터가 생성될 수 있기에 atomic함수로 원자화
        with transaction.atomic():
            new_system_info = serializer.save(user=request.user)

            # 요청받은 데이터 중 ref_boos, ref_datas의 pk리스트를 받음
            # pk리스트의 원소가 존재한다면 해당 pk의 객체들을 `new_system_info` 객체와 연결
            for field_name in ["ref_books_pk", "ref_datas_pk"]:
                if field_name in request.data:
                    try:
                        pk_list = json.loads(request.data[field_name])
                        related_model = (
                            RefBook if field_name == "ref_books_pk" else RefData
                        )
                        related_objects = [
                            related_model.objects.get(pk=pk) for pk in pk_list
                        ]

                        # getattr을 통해 new_system_info의 ref_book(or ref_datas) 필드를 불러옵니다.
                        # ForeignKey이기 때문에 set() 함수를 통해 객체리스트를 지정합니다.
                        getattr(new_system_info, field_name.replace("_pk", "")).set(
                            related_objects
                        )
                    except:
                        raise exceptions.ParseError(f"참조 {related_model.__name__} 에러")

            return Response(status=status.HTTP_201_CREATED)


class SystemInfosList(APIView):
    """요약된 SystemInfo 리스트 APIView"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """SystemInfo 리스트 요청 함수

        Parameters:
            queryset (list(SystemInfo)) : 유저가 가진 SystemInfo 리스트
            paginated_system_infos (list(SystemInfo)) : 유저가 가진 SystemInfo 리스트를 페이지네이션한 리스트

        Returns:
            Response : 페이지별 데이터 및 상태 반환
        """
        queryset = SystemInfo.objects.filter(user=request.user)
        pagination = PageNumberPagination()
        paginated_system_infos = pagination.paginate_queryset(
            queryset,
            request,
        )

        serializer = serializers.SystemInfoListSerializer(
            paginated_system_infos,
            many=True,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class SystemInfoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            system_info = SystemInfo.objects.get(pk=pk)
            return system_info
        except:
            raise exceptions.NotFound()

    def get(self, request, pk):
        system_info = self.get_object(pk)
        serializer = serializers.SystemInfoDetailSerializer(system_info)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        system_info = self.get_object(pk)

        serializer = serializers.CreateSystemInfoSerializer(
            system_info,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            update_system_info = serializer.save()
            for field_name in ["ref_books_pk", "ref_datas_pk"]:
                if field_name in request.data:
                    try:
                        pk_list = json.loads(request.data[field_name])
                        related_model = (
                            RefBook if field_name == "ref_books_pk" else RefData
                        )
                        related_objects = [
                            related_model.objects.get(pk=int(pk)) for pk in pk_list
                        ]
                        getattr(update_system_info, field_name.replace("_pk", "")).set(
                            related_objects
                        )
                    except:
                        raise exceptions.ParseError(f"참조 {related_model.__name__} 에러")
        return Response(
            serializers.SystemInfoDetailSerializer(update_system_info).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        system_info = self.get_object(pk)
        system_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DialogueDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return SystemInfo.objects.get(pk=pk)
        except:
            raise exceptions.NotFound("Not Found System Information")

    def get(self, request, pk):
        system_info = self.get_object(pk)
        serializer = serializers.SystemInfoDetailSerializer(system_info)
        dialogues = self.generate_dialogue(system_info=serializer.data)

        return Response(dialogues, status=status.HTTP_200_OK)

    def generate_dialogue(self, system_info):
        level = {
            1: "freshman",
            2: "sophomore",
            3: "junior",
            4: "senior",
            5: "graduate student",
        }
        language = "Korean" if system_info["language"] == "ko" else "English"
        major = system_info["major"]
        understanding_level = level[system_info["understanding_level"]]
        only_use_reference_data = system_info["only_use_reference_data"]
        ref_books = system_info["ref_books"]
        ref_datas = system_info["ref_datas"]
        data_sequence = system_info["data_sequence"]

        dialogue_list = []
        ## system role 설정
        dialogue_list.append(
            f"I would like your system to take on the role of teaching college students. Your major is {major}, and the level of teaching is around {understanding_level} year."
        )

        # 참고 서적 설정
        if ref_books:
            dialogue_list.append(
                f"I will now inform you of the book I'm using. And I will state them in the format of 'Author - Title'. Please gather my information until I say 'I have finished providing reference books.' Use the book to respond to me."
            )
            for ref_book in ref_books:
                dialogue_list.append(f"'{ref_book['author']} - {ref_book['title']}', ")
            dialogue_list.append("I have finished providing reference books.")

        if ref_datas:
            user_role_data_content = 'I have reference materials. Each piece of material is enclosed within three double quotation marks in the following format:"""title: , content: """.  Please gather my information until I say "I have finished providing reference materials."'
            if data_sequence:
                user_role_data_content += " There is an order in the materials. You will receive them in sequence."

            if only_use_reference_data:
                user_role_data_content += " Please prioritize responses based on the reference materials I've sent for now."
            dialogue_list.append(user_role_data_content)

            for ref_data in ref_datas:
                dialogue_list.append(
                    f'"""title: {ref_data["title"]}, content: {ref_data["text"]}"""'
                )
            dialogue_list.append("I have finished providing reference materials")

        dialogue_list.append(
            f"After starting this chat with you, I have provided information about myself and the reference materials you will use."
        )
        dialogue_list.append(
            f"From now on, please respond only in {language}, regardless of the language I use."
        )

        return dialogue_list


class CreateRefBook(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializers.CreateRefBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class RefBooksList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = RefBook.objects.filter(user=request.user)
        pagination = PageNumberPagination()
        paginated_ref_books = pagination.paginate_queryset(
            queryset,
            request,
        )

        serializer = serializers.RefBookListSerializer(
            paginated_ref_books,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class RefBookDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return RefBook.objects.get(pk=pk)
        except:
            raise exceptions.NotFound()

    def put(self, request, pk):
        ref_book = self.get_object(pk)
        serializer = serializers.CreateRefBookSerializer(
            ref_book,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        ref_book = self.get_object(pk)
        ref_book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateRefData(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ref_data_serializer = serializers.CreateRefDataSerializer(data=request.data)
        content_serializer = serializers.RefDataContentSerializer(data=request.data)

        if not ref_data_serializer.is_valid():
            return Response(
                ref_data_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not content_serializer.is_valid():
            return Response(
                content_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_ref_data = ref_data_serializer.save(user=request.user)
        content_serializer.save(data=new_ref_data)

        return Response(status=status.HTTP_201_CREATED)


class RefDatasList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = RefData.objects.filter(user=request.user)
        pagination = PageNumberPagination()
        paginated_ref_datas = pagination.paginate_queryset(
            queryset,
            request,
        )

        serializer = serializers.RefDataListSerializer(
            paginated_ref_datas,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class RefDataDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return RefData.objects.get(pk=pk)
        except:
            raise exceptions.NotFound()

    def put(self, request, pk):
        ref_data = self.get_object(pk)
        ref_data_serializer = serializers.RefDataListSerializer(
            ref_data,
            data=request.data,
            partial=True,
        )
        content_serializer = serializers.RefDataContentSerializer(
            ref_data.content,
            data=request.data,
            partial=True,
        )
        if not ref_data_serializer.is_valid():
            return Response(
                ref_data_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not content_serializer.is_valid():
            return Response(
                content_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        ref_data_serializer.save()
        content_serializer.save()

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        ref_data = self.get_object(pk)
        ref_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
