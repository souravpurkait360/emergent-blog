from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Extends simplejwt to include user data in the token response."""

    def validate(self, attrs):
        from apps.accounts.serializers.user_serializer import UserSerializer

        token_data = super().validate(attrs)
        token_data["user"] = UserSerializer(self.user).data
        return token_data
