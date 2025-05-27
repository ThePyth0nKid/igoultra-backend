from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.serializers import SocialLoginSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "ultra_name",
            "level",
            "xp",
            "rank",
            "avatar_url",
        ]

class DiscordJWTSerializer(SocialLoginSerializer):
    """
    Extends the dj-rest-auth SocialLoginSerializer to
    issue JWT access & refresh tokens after Discord OAuth login.
    """
    def validate(self, attrs):
        # Perform the usual social login (creates/gets user)
        data = super().validate(attrs)

        # Generate JWT refresh & access tokens for that user
        user = self.context['request'].user
        refresh = RefreshToken.for_user(user)
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)

        return data
