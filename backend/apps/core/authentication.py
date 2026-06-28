"""Cookie-based JWT authentication for httpOnly token storage.

Reads JWT from httpOnly cookies first, then falls back to Authorization header.
This ensures sensitive tokens are never exposed to JavaScript (XSS protection).
"""
import logging

from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger(__name__)

COOKIE_ACCESS_TOKEN_KEY = "access_token"


class CookieJWTAuthentication(JWTAuthentication):
    """JWT authentication that supports httpOnly cookies.

    Priority: Authorization header > access_token cookie.
    This class is a singleton via Django's authentication backend caching.
    """

    def authenticate(self, request):
        # Try the standard Authorization header first (Postman / API tools)
        header = self.get_header(request)
        if header is not None:
            return super().authenticate(request)

        # Fall back to httpOnly cookie
        raw_token = request.COOKIES.get(COOKIE_ACCESS_TOKEN_KEY)
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token.encode())
            user = self.get_user(validated_token)
            return user, validated_token
        except Exception as exc:
            logger.debug("Cookie JWT authentication failed: %s", exc)
            return None
