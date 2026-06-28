import logging

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.serializers.user_serializer import UserSerializer
from apps.accounts.services.user_service import UserService

logger = logging.getLogger(__name__)


class UserListAPIView(APIView):
    """GET /api/auth/users/ – list all users (admin only)."""

    permission_classes = [permissions.IsAdminUser]

    def get(self, request: Request) -> Response:
        user_service = UserService.get_instance()
        all_users = user_service.get_all_users()
        return Response(UserSerializer(all_users, many=True, context={"request": request}).data)
