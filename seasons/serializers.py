from rest_framework import serializers
from .models import Season, SeasonXp

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ["id", "name", "start", "end", "is_active"]

class SeasonXpSerializer(serializers.ModelSerializer):
    season = SeasonSerializer(read_only=True)
    class Meta:
        model = SeasonXp
        fields = ["season", "xp"]
