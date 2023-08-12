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


class SignInAPITest(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "password": "testpassword123",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_valid_signin(self):
        response = self.client.post(
            reverse("signin"),
            self.user_data,
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertIn("token", response.data)

    def test_invalid_signin_missing_data(self):
        invalid_data = {"username": "", "password": ""}
        response = self.client.post(
            reverse("signin"),
            invalid_data,
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_invalid_signin_wrong_credentials(self):
        invalid_credentials = {
            "username": "testuser",
            "password": "wrongpassword",
        }
        response = self.client.post(
            reverse("signin"),
            invalid_credentials,
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("error", response.data)


class APITestCase(APITestCase):
    def test_urls_exist(self):
        urls = [
            reverse("signup"),
            reverse("signin"),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
