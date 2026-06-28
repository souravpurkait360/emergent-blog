import logging

from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.cookies import COOKIE_REFRESH_KEY, clear_auth_cookies, set_auth_cookies

logger = logging.getLogger(__name__)


class TokenRefreshAPIView(APIView):
    """POST /api/auth/token/refresh/ – issue a new access token using the refresh cookie."""

    permission_classes = [permissions.AllowAny]

    def post(self, request: Request) -> Response:
        refresh_token_value = request.COOKIES.get(COOKIE_REFRESH_KEY)
        if not refresh_token_value:
            return Response({"error": "No refresh token cookie found"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh_token = RefreshToken(refresh_token_value)
            new_access_token = str(refresh_token.access_token)
            response = Response({"message": "Token refreshed successfully"})
            set_auth_cookies(response, new_access_token, refresh_token_value)
            return response
        except Exception as exc:
            logger.debug("Token refresh failed: %s", exc)
            response = Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
            clear_auth_cookies(response)
            return response
