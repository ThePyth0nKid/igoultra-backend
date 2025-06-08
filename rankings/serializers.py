# rankings/serializers.py

from rest_framework import serializers
from .models import LayerRankingEntry

class LayerRankingEntrySerializer(serializers.ModelSerializer):
    """
    Serializer für Leaderboard-Einträge:
    Gibt user (StringRelatedField), xp, real_layer und cyber_layer aus.
    """
    user = serializers.StringRelatedField()

    class Meta:
        model = LayerRankingEntry
        fields = ["user", "xp", "real_layer", "cyber_layer"]
