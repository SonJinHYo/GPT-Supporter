import json
from django.urls import reverse
from django.conf import settings

from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from .models import Content, RefData, SystemInfo


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import RefBook


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


class SystemInfoDetailTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.ref_book = RefBook.objects.create(
            user=self.user, author="Test Author", title="Test Title"
        )
        self.ref_data = RefData.objects.create(user=self.user, title="Test Title")
        self.ref_data_content = Content.objects.create(
            data=self.ref_data, text="Test Text"
        )
        self.system_info = SystemInfo.objects.create(
            description="Test Description",
            language="en",
            major="Computer Science",
            understanding_level=3,
            only_use_reference_data=True,
            user=self.user,
        )
        self.system_info.ref_books.add(self.ref_book)
        self.system_info.ref_datas.add(self.ref_data)
        self.url = reverse("detail", kwargs={"pk": self.system_info.pk})
        self.client.force_authenticate(user=self.user)

    def test_get_system_info(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], self.system_info.description)
        self.assertEqual(response.data["language"], self.system_info.language)
        self.assertEqual(response.data["major"], self.system_info.major)
        self.assertEqual(
            response.data["understanding_level"], self.system_info.understanding_level
        )
        self.assertEqual(
            response.data["only_use_reference_data"],
            self.system_info.only_use_reference_data,
        )
        self.assertEqual(response.data["ref_books"][0]["title"], self.ref_book.title)
        self.assertEqual(response.data["ref_datas"][0]["title"], self.ref_data.title)

    def test_update_system_info(self):
        updated_data = {
            "description": "Updated Description",
            "language": "ko",
            "major": "Electrical Engineering",
            "understanding_level": 4,
            "only_use_reference_data": False,
            "ref_books_pk": json.dumps([]),  # 빈 리스트로 업데이트
            "ref_datas_pk": json.dumps([self.ref_data.pk]),  # 기존 RefData 유지, RefBook 제거
        }
        response = self.client.put(self.url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.system_info.refresh_from_db()  # 데이터베이스에서 최신 정보로 업데이트
        self.assertEqual(self.system_info.description, updated_data["description"])
        self.assertEqual(self.system_info.language, updated_data["language"])
        self.assertEqual(self.system_info.major, updated_data["major"])
        self.assertEqual(
            self.system_info.understanding_level, updated_data["understanding_level"]
        )
        self.assertEqual(
            self.system_info.only_use_reference_data,
            updated_data["only_use_reference_data"],
        )
        self.assertEqual(self.system_info.ref_books.count(), 0)  # RefBook이 제거되었으므로 0
        self.assertEqual(self.system_info.ref_datas.first(), self.ref_data)

    def test_delete_system_info(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SystemInfo.objects.filter(pk=self.system_info.pk).exists())
