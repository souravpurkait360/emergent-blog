import logging

from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ai.services.ai_service import AIService

logger = logging.getLogger(__name__)


class AIAssistAPIView(APIView):
    """POST /api/ai/assist/ – generate a writing continuation for a blog post."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        try:
            title = request.data.get("title", "")
            existing_content = request.data.get("content", "")
            suggestion = AIService.get_instance().generate_writing_assistance(title, existing_content)
            return Response({"suggestion": suggestion})
        except Exception as exc:
            logger.exception("AI assist failed: %s", exc)
            return Response({"error": "AI assist unavailable"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
