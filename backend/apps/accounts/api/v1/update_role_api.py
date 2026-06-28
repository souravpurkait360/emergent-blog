import logging

from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.serializers.user_serializer import UserSerializer
from apps.accounts.services.user_service import UserService
from apps.core.exceptions import BlogAPIException

logger = logging.getLogger(__name__)


class UpdateUserRoleAPIView(APIView):
    """PATCH /api/auth/users/<pk>/role/ - change a user's role (admin only)."""

    permission_classes = [permissions.IsAdminUser]

    def patch(self, request: Request, pk: int) -> Response:
        try:
            new_role = request.data.get("role", "")
            user_service = UserService.get_instance()
            updated_user = user_service.update_user_role(pk, new_role)
            return Response(UserSerializer(updated_user, context={"request": request}).data)
        except BlogAPIException as exc:
            return Response({"error": exc.message}, status=exc.status_code)
        except Exception as exc:
            logger.exception("Unexpected error updating role: %s", exc)
            return Response({"error": "Update failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
