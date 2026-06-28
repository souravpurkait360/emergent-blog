from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class RegisterAPIViewTest(TestCase):
    """Unit tests for POST /api/auth/register/."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.register_url = reverse("auth-register")

    def test_register_with_valid_data_returns_201(self) -> None:
        payload = {
            "email": "newuser@example.com",
            "password": "securepass123",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)

    def test_register_sets_httponly_cookies(self) -> None:
        payload = {"email": "cookie@example.com", "password": "securepass123"}
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access_token", response.cookies)
        self.assertIn("refresh_token", response.cookies)
        self.assertTrue(response.cookies["access_token"]["httponly"])

    def test_register_with_duplicate_email_returns_error(self) -> None:
        payload = {"email": "dup@example.com", "password": "pass123"}
        self.client.post(self.register_url, payload, format="json")
        response = self.client.post(self.register_url, payload, format="json")
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT])

    def test_register_with_short_password_returns_400(self) -> None:
        payload = {"email": "short@example.com", "password": "ab"}
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_without_email_returns_400(self) -> None:
        response = self.client.post(self.register_url, {"password": "pass123"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
