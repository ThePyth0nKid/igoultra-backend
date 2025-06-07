from rest_framework import serializers
from .models import XpType, XpEvent

class XpTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = XpType
        fields = ['key', 'display_name', 'xp_amount', 'unit', 'description']

class XpEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = XpEvent
        fields = ['id', 'amount', 'source', 'metadata', 'timestamp']

class AddXpSerializer(serializers.Serializer):
    key = serializers.CharField(help_text='XpType.key, z.B. "pushups"')
    amount_units = serializers.FloatField(help_text='Einheiten der Aktivität, z.B. 20 (Reps) oder 15 (Minuten)')
    metadata = serializers.JSONField(required=False, help_text='Optional rohe Nutzereingabe o.ä.')
