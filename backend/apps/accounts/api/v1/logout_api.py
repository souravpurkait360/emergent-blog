from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.cookies import clear_auth_cookies


class LogoutAPIView(APIView):
    """POST /api/auth/logout/ - clear auth cookies to invalidate the session."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        clear_auth_cookies(response)
        return response
