from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class LoginAPIViewTest(TestCase):
    """Unit tests for POST /api/auth/token/ login endpoint."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.login_url = reverse("auth-login")
        self.test_user = User.objects.create_user(
            email="login@example.com",
            username="loginuser",
            password="correctpass123",
        )

    def test_login_with_valid_credentials_returns_200(self) -> None:
        response = self.client.post(
            self.login_url,
            {"email": "login@example.com", "password": "correctpass123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user", response.data)
        self.assertNotIn("access", response.data)  # Token moved to cookie
        self.assertNotIn("refresh", response.data)  # Token moved to cookie

    def test_login_sets_httponly_cookies(self) -> None:
        response = self.client.post(
            self.login_url,
            {"email": "login@example.com", "password": "correctpass123"},
            format="json",
        )
        self.assertIn("access_token", response.cookies)
        self.assertTrue(response.cookies["access_token"]["httponly"])

    def test_login_with_wrong_password_returns_401(self) -> None:
        response = self.client.post(
            self.login_url,
            {"email": "login@example.com", "password": "wrongpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_unknown_email_returns_401(self) -> None:
        response = self.client.post(
            self.login_url,
            {"email": "ghost@example.com", "password": "anypassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
