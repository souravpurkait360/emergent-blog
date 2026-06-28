from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Read serializer - output DTO for user data."""

    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "bio",
            "avatar_url",
            "role",
            "date_joined",
        ]
        read_only_fields = ["id", "date_joined", "role"]

    def get_avatar_url(self, user_obj):
        if user_obj.avatar:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(user_obj.avatar.url)
        return None
