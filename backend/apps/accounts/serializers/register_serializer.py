from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    """Input DTO for user registration."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    username = serializers.CharField(required=False, allow_blank=True, default="")
    first_name = serializers.CharField(required=False, allow_blank=True, default="")
    last_name = serializers.CharField(required=False, allow_blank=True, default="")

    def validate_email(self, email_value: str) -> str:
        if User.objects.filter(email=email_value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email_value


class TokenObtainSerializer(serializers.Serializer):
    """Input DTO for login."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
