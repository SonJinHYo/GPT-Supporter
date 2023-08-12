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
        self.url = reverse("signin")

    def test_valid_signin(self):
        response = self.client.post(
            self.url,
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
            self.url,
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
            self.url,
            invalid_credentials,
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("error", response.data)


class MeAPITest(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "password": "testpassword123",
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.login(
            username=self.user_data["username"],
            password=self.user_data["password"],
        )
        self.url = reverse("me")

    def test_get_user_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user_data["username"])

    def test_update_user_profile_valid_data(self):
        updated_data = {
            "email": "new_email@example.com",
            "using_token": 123,
        }
        response = self.client.put(
            self.url,
            updated_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()  # 데이터베이스 업데이트
        self.assertEqual(self.user.email, updated_data["email"])
        self.assertEqual(self.user.using_token, updated_data["using_token"])

    def test_update_user_profile_invalid_data(self):
        invalid_data = {
            "email": "invalid_email",
            "using_token": "invalid_value",
        }
        response = self.client.put(
            self.url,
            invalid_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
