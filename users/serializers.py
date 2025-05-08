from rest_framework import serializers
from .models import User

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
