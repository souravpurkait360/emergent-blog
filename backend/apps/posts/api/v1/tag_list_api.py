from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.posts.serializers.category_tag_serializers import TagSerializer
from apps.posts.services.category_service import TagService


class TagListAPIView(APIView):
    """GET /api/tags/ - list all tags."""

    permission_classes = [permissions.AllowAny]

    def get(self, request: Request) -> Response:
        tags = TagService.get_instance().get_all()
        return Response(TagSerializer(tags, many=True).data)
