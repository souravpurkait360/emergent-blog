import logging

from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.exceptions import BlogAPIException
from apps.posts.services.comment_service import CommentService

logger = logging.getLogger(__name__)


class CommentDeleteAPIView(APIView):
    """DELETE /api/comments/<pk>/ - remove a comment (own or admin)."""

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request: Request, pk: int) -> Response:
        try:
            CommentService.get_instance().delete_comment(pk, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BlogAPIException as exc:
            return Response({"error": exc.message}, status=exc.status_code)
        except Exception as exc:
            logger.exception("Comment delete failed for id %d: %s", pk, exc)
            return Response({"error": "Delete failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
