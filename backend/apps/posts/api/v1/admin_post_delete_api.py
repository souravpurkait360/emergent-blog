import logging

from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.exceptions import BlogAPIException
from apps.posts.repositories.post_repository import PostRepository

logger = logging.getLogger(__name__)


class AdminPostDeleteAPIView(APIView):
    """DELETE /api/posts/admin/<pk>/ - hard delete any post (admin only)."""

    permission_classes = [permissions.IsAdminUser]

    def delete(self, request: Request, pk: int) -> Response:
        try:
            post_repository = PostRepository.get_instance()
            post = post_repository.get_by_id(pk)
            post_repository.delete(post)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BlogAPIException as exc:
            return Response({"error": exc.message}, status=exc.status_code)
        except Exception as exc:
            logger.exception("Admin post delete failed for id %d: %s", pk, exc)
            return Response({"error": "Delete failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
