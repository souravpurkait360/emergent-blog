from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.posts.models import Post

User = get_user_model()


class PostDetailAPIViewTest(TestCase):
    """Integration tests for GET/PATCH/DELETE /api/posts/<slug>/."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.author = User.objects.create_user(email="author2@example.com", username="author2", password="pass123")
        self.other_user = User.objects.create_user(email="other@example.com", username="other", password="pass123")
        self.post = Post.objects.create(
            title="Detail Test Post", content="Some content", author=self.author, status="published"
        )
        self.detail_url = reverse("posts-detail", kwargs={"slug": self.post.slug})

        refresh = RefreshToken.for_user(self.author)
        self.client.cookies["access_token"] = str(refresh.access_token)

    def test_get_published_post_returns_200(self) -> None:
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Detail Test Post")

    def test_get_post_increments_views(self) -> None:
        initial_views = self.post.views
        self.client.get(self.detail_url)
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, initial_views + 1)

    def test_owner_can_delete_post(self) -> None:
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_owner_cannot_delete_post(self) -> None:
        other_client = APIClient()
        other_refresh = RefreshToken.for_user(self.other_user)
        other_client.cookies["access_token"] = str(other_refresh.access_token)
        response = other_client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
