import logging

from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.exceptions import BlogAPIException
from apps.posts.serializers.comment_serializer import CommentSerializer
from apps.posts.services.comment_service import CommentService

logger = logging.getLogger(__name__)


class CommentCreateAPIView(APIView):
    """POST /api/posts/<slug>/comments/ - add a comment to a post."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, slug: str) -> Response:
        try:
            comment_content = request.data.get("content", "").strip()
            if not comment_content:
                return Response({"error": "Comment content is required"}, status=status.HTTP_400_BAD_REQUEST)
            comment_service = CommentService.get_instance()
            new_comment = comment_service.add_comment(slug, request.user, comment_content)
            return Response(CommentSerializer(new_comment).data, status=status.HTTP_201_CREATED)
        except BlogAPIException as exc:
            return Response({"error": exc.message}, status=exc.status_code)
        except Exception as exc:
            logger.exception("Comment creation failed: %s", exc)
            return Response({"error": "Comment creation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
