import logging

from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.serializers.user_serializer import UserSerializer
from apps.accounts.services.user_service import UserService
from apps.core.cookies import set_auth_cookies
from apps.core.exceptions import BlogAPIException

logger = logging.getLogger(__name__)


class RegisterAPIView(APIView):
    """POST /api/auth/register/ – create a new user account."""

    permission_classes = [permissions.AllowAny]

    def post(self, request: Request) -> Response:
        try:
            user_service = UserService.get_instance()
            user, access_token, refresh_token = user_service.register_user(request.data)
            response = Response(
                {"user": UserSerializer(user, context={"request": request}).data},
                status=status.HTTP_201_CREATED,
            )
            set_auth_cookies(response, access_token, refresh_token)
            return response
        except BlogAPIException as exc:
            return Response({"error": exc.message}, status=exc.status_code)
        except Exception as exc:
            logger.exception("Unexpected error during registration: %s", exc)
            return Response({"error": "Registration failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
