from rest_framework import serializers
from seasons.models import Season, SeasonXp

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['id', 'name', 'start', 'end', 'is_active']

class SeasonXpSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = SeasonXp
        fields = ['user', 'xp', 'layer_type']
