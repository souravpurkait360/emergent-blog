from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.repositories.user_repository import UserRepository
from apps.accounts.serializers.register_serializer import RegisterSerializer
from apps.core.enums import UserRole
from apps.core.exceptions import ConflictException, NotFoundException, ValidationException

User = get_user_model()


class UserService:
    """Singleton service containing user account business logic."""

    _instance = None

    @classmethod
    def get_instance(cls) -> "UserService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        self._user_repository = UserRepository.get_instance()

    def register_user(self, data: dict) -> tuple[User, str, str]:
        """Create a new user account and return (user, access_token, refresh_token)."""
        serializer = RegisterSerializer(data=data)
        if not serializer.is_valid():
            raise ValidationException(str(serializer.errors))

        validated = serializer.validated_data
        email = validated["email"]
        password = validated["password"]
        username = validated.get("username") or email.split("@")[0]

        # Ensure username uniqueness
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = self._user_repository.create_user(
            email=email,
            password=password,
            username=username,
            first_name=validated.get("first_name", ""),
            last_name=validated.get("last_name", ""),
        )

        refresh = RefreshToken.for_user(user)
        return user, str(refresh.access_token), str(refresh)

    def update_user_role(self, user_id: int, new_role: str) -> User:
        """Update the role of an existing user."""
        try:
            role_enum = UserRole(new_role)
        except ValueError:
            raise ValidationException(f"Invalid role '{new_role}'")
        return self._user_repository.update_role(user_id, role_enum)

    def get_all_users(self):
        return self._user_repository.get_all_users()
