from django.urls import reverse
from django.conf import settings

from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from .models import RefData, SystemInfo


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


class RefBookDetailTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.ref_book = RefBook.objects.create(author="Test Author", title="Test Title")
        self.url = reverse("refbook-detail", kwargs={"pk": self.ref_book.pk})
        self.client.force_authenticate(user=self.user)

    def test_update_ref_book(self):
        updated_data = {"author": "Updated Author", "title": "Updated Title"}
        response = self.client.put(self.url, updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ref_book.refresh_from_db()  # 데이터베이스에서 최신 정보로 업데이트
        self.assertEqual(self.ref_book.author, updated_data["author"])
        self.assertEqual(self.ref_book.title, updated_data["title"])

    def test_delete_ref_book(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RefBook.objects.filter(pk=self.ref_book.pk).exists())


class CreateRefDataTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.url = reverse("create-refdata")  # 해당 URL 생성
        self.client.force_authenticate(user=self.user)

    def test_create_ref_data(self):
        data = {"title": "Test Title", "text": "Test Text"}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RefData.objects.count(), 1)
        self.assertEqual(RefData.objects.first().title, data["title"])
        self.assertEqual(RefData.objects.first().content.text, data["text"])

    def test_create_ref_data_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        invalid_data = {
            "title": "Test Title",
            # "text": "Test Text"  # text 필드가 누락된 무효한 데이터
        }
        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(RefData.objects.count(), 0)


class RefDatasListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.url = reverse("refdata")  # 해당 URL 생성

        self.page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]
        self.obj_count = 26
        self.last_page = self.obj_count // self.page_size + 1
        self.rem_page = self.obj_count % self.page_size

        # 10개의 RefData 인스턴스 생성
        for i in range(self.obj_count):
            self.client.post(
                reverse("create-refdata"),
                {
                    "title": f"Title {i}",
                    "content": f"Content {i}",
                },
            )
            # RefData.objects.create(title=f"Title {i}", content=f"Content {i}")

    def test_list_ref_datas(self):
        response = self.client.get(self.url)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Title 0")
        self.assertEqual(response.data[4]["title"], "Title 4")

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
