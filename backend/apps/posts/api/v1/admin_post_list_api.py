from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.posts.serializers.post_serializers import PostListSerializer
from apps.posts.services.post_service import PostService

PAGE_SIZE = 9


class AdminPostListAPIView(APIView):
    """GET /api/posts/admin/ - all posts for admin management."""

    permission_classes = [permissions.IsAdminUser]

    def get(self, request: Request) -> Response:
        post_service = PostService.get_instance()
        all_posts = post_service.get_all_posts()
        return Response(
            {
                "count": all_posts.count(),
                "results": PostListSerializer(all_posts, many=True, context={"request": request}).data,
            }
        )
