from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.posts.models import Post

User = get_user_model()


class CommentAPITest(TestCase):
    """Integration tests for comment create and delete endpoints."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="commenter@example.com", username="commenter", password="pass123"
        )
        self.post = Post.objects.create(
            title="Comment Target Post",
            content="Some content",
            author=self.user,
            status="published",
        )
        self.create_url = reverse("comments-create", kwargs={"slug": self.post.slug})
        refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.cookies["access_token"] = str(refresh.access_token)

    def test_authenticated_user_can_post_comment(self) -> None:
        response = self.client.post(self.create_url, {"content": "Great post!"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "Great post!")

    def test_empty_comment_returns_400(self) -> None:
        response = self.client.post(self.create_url, {"content": "  "}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_user_cannot_comment(self) -> None:
        anon_client = APIClient()
        response = anon_client.post(self.create_url, {"content": "Hello"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_delete_own_comment(self) -> None:
        create_response = self.client.post(self.create_url, {"content": "To delete"}, format="json")
        comment_id = create_response.data["id"]
        delete_url = reverse("comments-delete", kwargs={"pk": comment_id})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
