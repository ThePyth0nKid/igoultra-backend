from rest_framework import serializers
from .models import Layer, UserLayerProgress

class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer
        fields = ['id', 'code', 'name', 'type', 'order', 'description', 'essence', 'player_action']

class UserLayerProgressSerializer(serializers.ModelSerializer):
    real_layer = LayerSerializer(read_only=True)
    cyber_layer = LayerSerializer(read_only=True)

    class Meta:
        model = UserLayerProgress
        fields = ['id', 'user', 'real_layer', 'cyber_layer', 'updated_at'] 