from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from apps.core.enums import UserRole
from apps.core.exceptions import NotFoundException

User = get_user_model()


class UserRepository:
    """Singleton repository for User model data access.

    All ORM queries are centralised here; no ORM calls allowed in service or API layers.
    """

    _instance = None

    @classmethod
    def get_instance(cls) -> "UserRepository":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_all_users(self) -> QuerySet:
        return User.objects.all().order_by("-date_joined")

    def get_user_by_email(self, email: str) -> User:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist as exc:
            raise NotFoundException(f"User with email '{email}' not found") from exc

    def get_user_by_id(self, user_id: int) -> User:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist as exc:
            raise NotFoundException(f"User with id '{user_id}' not found") from exc

    def email_exists(self, email: str) -> bool:
        return User.objects.filter(email=email).exists()

    def create_user(self, email: str, password: str, username: str, **kwargs) -> User:
        return User.objects.create_user(
            email=email,
            username=username,
            password=password,
            **kwargs,
        )

    def update_role(self, user_id: int, new_role: UserRole) -> User:
        user = self.get_user_by_id(user_id)
        user.role = new_role
        user.is_staff = new_role == UserRole.ADMIN
        user.is_superuser = new_role == UserRole.ADMIN
        user.save(update_fields=["role", "is_staff", "is_superuser"])
        return user

    def update_profile(self, user: User, **fields) -> User:
        for field_name, field_value in fields.items():
            setattr(user, field_name, field_value)
        user.save()
        return user
