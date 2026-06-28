from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.posts.serializers.post_serializers import PostListSerializer
from apps.posts.services.post_service import PostService


class MyPostsAPIView(APIView):
    """GET /api/posts/my/ – list the authenticated user's own posts."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        post_service = PostService.get_instance()
        posts = post_service.get_user_posts(request.user)
        return Response({
            "count": posts.count(),
            "results": PostListSerializer(posts, many=True, context={"request": request}).data,
        })
