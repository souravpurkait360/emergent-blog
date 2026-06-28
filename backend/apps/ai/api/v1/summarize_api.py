import logging

from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ai.services.ai_service import AIService

logger = logging.getLogger(__name__)


class AISummarizeAPIView(APIView):
    """POST /api/ai/summarize/ – generate an AI summary for a blog post."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        try:
            title = request.data.get("title", "")
            content = request.data.get("content", "")
            summary = AIService.get_instance().generate_summary(title, content)
            return Response({"summary": summary})
        except Exception as exc:
            logger.exception("AI summarize failed: %s", exc)
            return Response({"error": "AI summarize unavailable"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
