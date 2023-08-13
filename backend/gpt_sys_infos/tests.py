from django.urls import reverse
from django.conf import settings

from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from .models import SystemInfo


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import RefBook
from .serializers import CreateRefBookSerializer


class CreateRefBookTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.url = reverse("create-refbook")

    def test_create_ref_book(self):
        self.client.force_authenticate(user=self.user)
        data = {"author": "Test Author", "title": "Test Title"}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RefBook.objects.count(), 1)
        self.assertEqual(RefBook.objects.first().author, data["author"])
        self.assertEqual(RefBook.objects.first().title, data["title"])

    def test_create_ref_book_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        invalid_data = {
            "author": "Test Author",
            # "title": "Test Title",
        }
        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(RefBook.objects.count(), 0)  # 무효한 데이터로 인해 생성되지 않아야 함


class RefBooksListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.ref_book_1 = RefBook.objects.create(author="Author 1", title="Title 1")
        self.ref_book_2 = RefBook.objects.create(author="Author 2", title="Title 2")

        self.url = reverse("refbook")

        self.page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]
        self.obj_count = 26
        self.last_page = self.obj_count // self.page_size + 1
        self.rem_page = self.obj_count % self.page_size

        for i in range(3, self.obj_count + 1):
            RefBook.objects.create(author=f"Author {i}", title=f"Title {i}")

    def test_list_ref_books(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["author"], self.ref_book_1.author)
        self.assertEqual(response.data[0]["title"], self.ref_book_1.title)
        self.assertEqual(response.data[1]["author"], self.ref_book_2.author)
        self.assertEqual(response.data[1]["title"], self.ref_book_2.title)

    def test_pagination_ref_books(self):
        for page in range(1, self.last_page + 1):
            response = self.client.get(f"{self.url}" + f"?page={page}")
            if page != self.last_page:
                self.assertEqual(len(response.data), self.page_size)
            else:
                self.assertEqual(len(response.data), self.rem_page)


# class CreateSysInfoTest(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="testuser", password="testpassword"
#         )
#         self.client.force_authenticate(user=self.user)
#         self.url = reverse("create-sysinfo")  # create-sys-info는 실제 URL 패턴에 맞게 수정해야 함

#     def test_create_sys_info_success(self):
#         data = {
#             "description": "Test description",
#             "language": "ko",
#             "major": "소프트웨어공학과",
#             "understanding_level": 4,
#             "only_use_reference_data": True,
#         }
#         response = self.client.post(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_create_sys_info_invalid_data(self):
#         data_list = [
#             {
#                 "description": "Test description",
#                 "language": "ko",
#                 "major": "소프트웨어공학과",
#                 "understanding_level": 4,
#                 "only_use_reference_data": "invalid_value",
#             },
#             {
#                 "description": "Test description",
#                 "language": "ko",
#                 "major": "소프트웨어공학과",
#                 "understanding_level": 8,
#                 "only_use_reference_data": False,
#             },
#             {
#                 "description": "Test description",
#                 "language": "kokorean",
#                 "major": "소프트웨어공학과",
#                 "understanding_level": 4,
#                 "only_use_reference_data": True,
#             },
#         ]
#         for data in data_list:
#             response = self.client.post(self.url, data, format="json")
#             self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class SysInfosListTest(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="testuser", password="testpassword"
#         )
#         self.client.force_authenticate(user=self.user)
#         self.url = reverse("sysinfo-list")  # sys-info-list는 실제 URL 패턴에 맞게 수정해야 함
#         self.page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]
#         self.obj_count = 26
#         self.last_page = self.obj_count // self.page_size + 1
#         self.rem_page = self.obj_count % self.page_size

#         # Create 24 sample SystemInfo objects for testing pagination
#         for i in range(1, self.obj_count + 1):
#             data = {
#                 "description": f"Test description{i}+1",
#                 "language": "ko",
#                 "major": "소프트웨어공학과",
#                 "understanding_level": 4,
#                 "only_use_reference_data": True,
#             }
#             self.client.post(reverse("create-sysinfo"), data, format="json")

#     def test_get_sys_infos_list(self):
#         for page in range(1, self.last_page + 1):
#             response = self.client.get(f"{self.url}?page={page}")
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#             if page != self.last_page:
#                 self.assertEqual(len(response.data), self.page_size)
#             else:
#                 self.assertEqual(len(response.data), self.rem_page)

#     def test_unauthenticated_access(self):
#         self.client.logout()
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
