import logging

from rest_framework import permissions, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.exceptions import BlogAPIException
from apps.posts.serializers.post_serializers import PostCreateSerializer, PostDetailSerializer
from apps.posts.services.post_service import PostService

logger = logging.getLogger(__name__)


class PostDetailAPIView(APIView):
    """GET/PATCH/DELETE /api/posts/<slug>/ - retrieve, update, or delete a post."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request: Request, slug: str) -> Response:
        try:
            post_service = PostService.get_instance()
            post = post_service.get_post(slug)
            post_service.record_view(post.pk)
            post.refresh_from_db(fields=["views"])
            return Response(PostDetailSerializer(post, context={"request": request}).data)
        except BlogAPIException as exc:
            return Response({"error": exc.message}, status=exc.status_code)

    def patch(self, request: Request, slug: str) -> Response:
        try:
            post_service = PostService.get_instance()
            input_serializer = PostCreateSerializer(data=request.data, partial=True)
            input_serializer.is_valid(raise_exception=True)
            updated_post = post_service.update_post(slug, request.user, input_serializer.validated_data)
            return Response(PostDetailSerializer(updated_post, context={"request": request}).data)
        except BlogAPIException as exc:
            return Response({"error": exc.message}, status=exc.status_code)
        except Exception as exc:
            logger.exception("Post update failed for slug '%s': %s", slug, exc)
            return Response({"error": "Update failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request: Request, slug: str) -> Response:
        try:
            PostService.get_instance().delete_post(slug, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BlogAPIException as exc:
            return Response({"error": exc.message}, status=exc.status_code)
