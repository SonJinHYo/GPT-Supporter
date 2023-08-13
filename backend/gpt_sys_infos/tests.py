import json
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

        self.url = reverse("refbook")

        self.page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]
        self.obj_count = 26
        self.last_page = self.obj_count // self.page_size + 1
        self.rem_page = self.obj_count % self.page_size

        for i in range(1, self.obj_count + 1):
            self.client.post(
                reverse("create-refbook"),
                {
                    "author": f"Author {i}",
                    "title": f"Title {i}",
                },
            )

    def test_list_ref_books(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        self.ref_book = RefBook.objects.create(
            user=self.user, author="Test Author", title="Test Title"
        )
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

        for i in range(1, self.obj_count + 1):
            self.client.post(
                reverse("create-refdata"),
                {
                    "title": f"Title {i}",
                    "text": f"Content {i}",
                },
            )

    def test_list_ref_datas(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pagination_ref_books(self):
        for page in range(1, self.last_page + 1):
            response = self.client.get(f"{self.url}" + f"?page={page}")
            if page != self.last_page:
                self.assertEqual(len(response.data), self.page_size)
            else:
                self.assertEqual(len(response.data), self.rem_page)


class RefDataDetailTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.client.post(
            reverse("create-refdata"),
            {
                "user": self.user,
                "title": "Test Title",
                "text": "Test Text",
            },
        )
        self.ref_data = RefData.objects.get(user=self.user, pk=1)
        self.url = reverse("refdata-detail", kwargs={"pk": self.ref_data.pk})

    def test_update_ref_data(self):
        updated_data = {"title": "Updated Title", "text": "Updated Text"}
        response = self.client.put(self.url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.ref_data.refresh_from_db()  # 데이터베이스에서 최신 정보로 업데이트
        self.assertEqual(self.ref_data.title, updated_data["title"])
        self.assertEqual(self.ref_data.content.text, updated_data["text"])

    def test_delete_ref_data(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RefData.objects.filter(pk=self.ref_data.pk).exists())


class CreateSystemInfoTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.ref_book = RefBook.objects.create(
            user=self.user,
            author="Test Author",
        )
        self.ref_data = RefData.objects.create(
            user=self.user,
            title="Test Title",
        )
        self.url = reverse("create-sysinfo")  # 해당 URL 생성

    def test_create_system_info(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "description": "Test Description",
            "language": "en",
            "major": "Computer Science",
            "understanding_level": 3,
            "only_use_reference_data": True,
            "ref_books_pk": json.dumps([self.ref_book.pk]),
            "ref_datas_pk": json.dumps([self.ref_data.pk]),
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SystemInfo.objects.count(), 1)
        new_system_info = SystemInfo.objects.first()
        self.assertEqual(new_system_info.description, data["description"])
        self.assertEqual(new_system_info.language, data["language"])
        self.assertEqual(new_system_info.major, data["major"])
        self.assertEqual(
            new_system_info.understanding_level, data["understanding_level"]
        )
        self.assertEqual(
            new_system_info.only_use_reference_data, data["only_use_reference_data"]
        )
        self.assertEqual(new_system_info.ref_books.first(), self.ref_book)
        self.assertEqual(new_system_info.ref_datas.first(), self.ref_data)

    def test_create_system_info_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        invalid_data = {
            "description": "Test Description",
            "language": "en",
            # 필요한 데이터가 누락된 무효한 데이터
        }
        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SystemInfo.objects.count(), 0)  # 무효한 데이터로 인해 생성되지 않아야 함


class SystemInfosListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.url = reverse("sysinfo-list")  # 해당 URL 생성

        self.page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]
        self.obj_count = 26
        self.last_page = self.obj_count // self.page_size + 1
        self.rem_page = self.obj_count % self.page_size

        for i in range(1, self.obj_count + 1):
            SystemInfo.objects.create(
                description=f"Description {i}",
                language="en",
                major="Computer Science",
                understanding_level=3,
                only_use_reference_data=True,
                user=self.user,
            )

    def test_list_system_infos(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pagination_sys_info_list(self):
        for page in range(1, self.last_page + 1):
            response = self.client.get(f"{self.url}" + f"?page={page}")
            if page != self.last_page:
                self.assertEqual(len(response.data), self.page_size)
            else:
                self.assertEqual(len(response.data), self.rem_page)
