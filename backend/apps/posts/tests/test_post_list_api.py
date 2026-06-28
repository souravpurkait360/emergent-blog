from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.posts.models import Category, Post

User = get_user_model()


class PostListAPIViewTest(TestCase):
    """Integration tests for GET/POST /api/posts/."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.list_url = reverse("posts-list")
        self.user = User.objects.create_user(email="author@example.com", username="author", password="pass123")
        self.category = Category.objects.create(name="Tech")
        self.post = Post.objects.create(
            title="Test Post",
            content="Content here",
            author=self.user,
            status="published",
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.cookies["access_token"] = str(refresh.access_token)

    def test_unauthenticated_can_list_published_posts(self) -> None:
        anon_client = APIClient()
        response = anon_client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_list_returns_correct_count(self) -> None:
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data["count"], 1)

    def test_search_filters_results(self) -> None:
        response = self.client.get(self.list_url, {"search": "Test Post"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [post["title"] for post in response.data["results"]]
        self.assertIn("Test Post", titles)

    def test_create_post_requires_auth(self) -> None:
        anon_client = APIClient()
        response = anon_client.post(self.list_url, {"title": "X", "content": "Y"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_post(self) -> None:
        payload = {"title": "New Post", "content": "Body text", "status": "draft"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Post")
