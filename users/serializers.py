from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from factions.models import Faction
from origins.models import Origin

class FactionShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faction
        fields = ["id", "name", "style", "icon"]

class OriginShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Origin
        fields = ["id", "name", "type"]

class UserSerializer(serializers.ModelSerializer):
    faction = FactionShortSerializer(read_only=True)
    faction_id = serializers.PrimaryKeyRelatedField(
        queryset=Faction.objects.all(), source="faction", write_only=True, required=False
    )
    origin = OriginShortSerializer(read_only=True)
    origin_id = serializers.PrimaryKeyRelatedField(
        queryset=Origin.objects.all(), source="origin", write_only=True, required=False
    )
    missing_onboarding_fields = serializers.SerializerMethodField()
    avatar = serializers.ImageField(required=False, allow_null=True)

    def get_missing_onboarding_fields(self, obj):
        missing = []
        if not obj.ultra_name:
            missing.append("ultra_name")
        if not obj.faction:
            missing.append("faction")
        if not obj.origin:
            missing.append("origin")
        if not obj.bio:
            missing.append("bio")
        if not obj.avatar_url:
            missing.append("avatar_url")
        return missing

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
            "avatar",
            "bio",
            "faction",
            "faction_id",
            "origin",
            "origin_id",
            "missing_onboarding_fields",
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
