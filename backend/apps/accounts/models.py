from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.enums import UserRole


class User(AbstractUser):
    """Extended user model with role-based access control."""

    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=[(role.value, role.value.capitalize()) for role in UserRole],
        default=UserRole.READER,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return self.email

    @property
    def is_admin_role(self) -> bool:
        return self.role == UserRole.ADMIN
