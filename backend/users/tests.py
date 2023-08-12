from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import User


class SignUpAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("signup")  # "signup" 이름의 URL을 가져옴

    def test_signup_valid_data(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(
            User.objects.get().username,
            "testuser",
        )

    def test_signup_missing_fields(self):
        data = {
            "username": "testuser",
            "password": "testpassword123",
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_signup_invalid_email(self):
        data = {
            "username": "testuser",
            "email": "invalid_email",
            "password": "testpassword123",
        }

        response = self.client.post(self.url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(User.objects.count(), 0)
