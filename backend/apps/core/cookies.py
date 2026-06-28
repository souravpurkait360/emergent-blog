"""Shared cookie utility helpers used across auth API views."""
import os

COOKIE_ACCESS_KEY = "access_token"
COOKIE_REFRESH_KEY = "refresh_token"
ACCESS_MAX_AGE = 86400       # 24 hours
REFRESH_MAX_AGE = 604800     # 7 days
SECURE_COOKIES = os.environ.get("SECURE_COOKIES", "true").lower() == "true"


def set_auth_cookies(response, access_token: str, refresh_token: str) -> None:
    """Attach httpOnly auth cookies to the given response object."""
    response.set_cookie(
        COOKIE_ACCESS_KEY,
        access_token,
        httponly=True,
        secure=SECURE_COOKIES,
        samesite="Lax",
        max_age=ACCESS_MAX_AGE,
    )
    response.set_cookie(
        COOKIE_REFRESH_KEY,
        refresh_token,
        httponly=True,
        secure=SECURE_COOKIES,
        samesite="Lax",
        max_age=REFRESH_MAX_AGE,
    )


def clear_auth_cookies(response) -> None:
    """Remove auth cookies from the given response object."""
    response.delete_cookie(COOKIE_ACCESS_KEY)
    response.delete_cookie(COOKIE_REFRESH_KEY)
