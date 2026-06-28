from django.urls import path

from apps.accounts.api.v1.login_api import LoginAPIView
from apps.accounts.api.v1.logout_api import LogoutAPIView
from apps.accounts.api.v1.me_api import MeAPIView
from apps.accounts.api.v1.register_api import RegisterAPIView
from apps.accounts.api.v1.token_refresh_api import TokenRefreshAPIView
from apps.accounts.api.v1.update_role_api import UpdateUserRoleAPIView
from apps.accounts.api.v1.user_list_api import UserListAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="auth-register"),
    path("token/", LoginAPIView.as_view(), name="auth-login"),
    path("token/refresh/", TokenRefreshAPIView.as_view(), name="auth-token-refresh"),
    path("logout/", LogoutAPIView.as_view(), name="auth-logout"),
    path("me/", MeAPIView.as_view(), name="auth-me"),
    path("users/", UserListAPIView.as_view(), name="auth-user-list"),
    path("users/<int:pk>/role/", UpdateUserRoleAPIView.as_view(), name="auth-update-role"),
]
