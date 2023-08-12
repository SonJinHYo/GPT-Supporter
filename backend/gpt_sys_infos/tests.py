from django.urls import reverse
from django.conf import settings

from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from .models import SystemInfo


class CreateSysInfoTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("create-sysinfo")  # create-sys-info는 실제 URL 패턴에 맞게 수정해야 함

    def test_create_sys_info_success(self):
        data = {
            "description": "Test description",
            "language": "ko",
            "major": "소프트웨어공학과",
            "understanding_level": 4,
            "only_use_reference_data": True,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_sys_info_invalid_data(self):
        data_list = [
            {
                "description": "Test description",
                "language": "ko",
                "major": "소프트웨어공학과",
                "understanding_level": 4,
                "only_use_reference_data": "invalid_value",
            },
            {
                "description": "Test description",
                "language": "ko",
                "major": "소프트웨어공학과",
                "understanding_level": 8,
                "only_use_reference_data": False,
            },
            {
                "description": "Test description",
                "language": "kokorean",
                "major": "소프트웨어공학과",
                "understanding_level": 4,
                "only_use_reference_data": True,
            },
        ]
        for data in data_list:
            response = self.client.post(self.url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SysInfosListTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("sysinfo-list")  # sys-info-list는 실제 URL 패턴에 맞게 수정해야 함
        self.page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]
        self.obj_count = 26
        self.last_page = self.obj_count // self.page_size + 1
        self.rem_page = self.obj_count % self.page_size

        # Create 24 sample SystemInfo objects for testing pagination
        for i in range(1, self.obj_count + 1):
            data = {
                "description": f"Test description{i}+1",
                "language": "ko",
                "major": "소프트웨어공학과",
                "understanding_level": 4,
                "only_use_reference_data": True,
            }
            self.client.post(reverse("create-sysinfo"), data, format="json")

    def test_get_sys_infos_list(self):
        for page in range(1, self.last_page + 1):
            response = self.client.get(f"{self.url}?page={page}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            if page != self.last_page:
                self.assertEqual(len(response.data), self.page_size)
            else:
                self.assertEqual(len(response.data), self.rem_page)

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
