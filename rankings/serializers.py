# rankings/serializers.py

from rest_framework import serializers
from .models import LayerRankingEntry

class LayerRankingEntrySerializer(serializers.ModelSerializer):
    """
    Serializer für Leaderboard-Einträge:
    Gibt user (StringRelatedField), xp, real_layer und cyber_layer aus.
    """
    user = serializers.StringRelatedField()
    real_layer = serializers.SerializerMethodField()
    cyber_layer = serializers.SerializerMethodField()

    class Meta:
        model = LayerRankingEntry
        fields = ["user", "xp", "real_layer", "cyber_layer"]

    def get_real_layer(self, obj):
        """Gibt den aktuellen Real-Layer des Users zurück"""
        try:
            return obj.user.userlayerprogress.real_layer.name
        except:
            return "Base"

    def get_cyber_layer(self, obj):
        """Gibt den aktuellen Cyber-Layer des Users zurück"""
        try:
            return obj.user.userlayerprogress.cyber_layer.name
        except:
            return "Surface-Web"
