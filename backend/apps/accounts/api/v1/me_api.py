from rest_framework import permissions
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.repositories.user_repository import UserRepository
from apps.accounts.serializers.user_serializer import UserSerializer
from apps.core.exceptions import BlogAPIException


class MeAPIView(APIView):
    """GET /api/auth/me/ - retrieve current user. PATCH - update profile."""

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request: Request) -> Response:
        return Response(UserSerializer(request.user, context={"request": request}).data)

    def patch(self, request: Request) -> Response:
        try:
            allowed_fields = {"first_name", "last_name", "bio", "avatar"}
            update_data = {key: value for key, value in request.data.items() if key in allowed_fields}
            user_repository = UserRepository.get_instance()
            updated_user = user_repository.update_profile(request.user, **update_data)
            return Response(UserSerializer(updated_user, context={"request": request}).data)
        except BlogAPIException as exc:
            return Response({"error": exc.message}, status=exc.status_code)
