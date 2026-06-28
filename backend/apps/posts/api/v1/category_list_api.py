import logging

from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.exceptions import BlogAPIException
from apps.posts.serializers.category_tag_serializers import CategorySerializer
from apps.posts.services.category_service import CategoryService

logger = logging.getLogger(__name__)


class CategoryListAPIView(APIView):
    """GET /api/categories/ – list all categories. POST – create (admin only)."""

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get(self, request: Request) -> Response:
        categories = CategoryService.get_instance().get_all()
        return Response(CategorySerializer(categories, many=True).data)

    def post(self, request: Request) -> Response:
        try:
            name = request.data.get("name", "")
            description = request.data.get("description", "")
            category = CategoryService.get_instance().create_category(name, description)
            return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)
        except BlogAPIException as exc:
            return Response({"error": exc.message}, status=exc.status_code)
