import logging

from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.serializers.token_serializer import CustomTokenObtainPairSerializer
from apps.core.cookies import set_auth_cookies

logger = logging.getLogger(__name__)


class LoginAPIView(TokenObtainPairView):
    """POST /api/auth/token/ – authenticate and receive httpOnly auth cookies."""

    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            access_token = response.data.pop("access", None)
            refresh_token = response.data.pop("refresh", None)
            if access_token and refresh_token:
                set_auth_cookies(response, access_token, refresh_token)
        return response
