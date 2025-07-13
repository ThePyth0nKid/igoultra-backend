from rest_framework import serializers
from .models import Season, Mission, MissionProgress

class SeasonSerializer(serializers.ModelSerializer):
    """Serializer für Seasons"""
    
    class Meta:
        model = Season
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class MissionSerializer(serializers.ModelSerializer):
    """Serializer für Missionen"""
    season = SeasonSerializer(read_only=True)
    season_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Mission
        fields = [
            'id', 'title', 'description', 'mission_type', 'unit', 'target_value',
            'xp_reward', 'gold_reward', 'ultra_point_reward',
            'start_time', 'end_time', 'season', 'season_id',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        season_id = validated_data.pop('season_id', None)
        if season_id:
            validated_data['season_id'] = season_id
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        season_id = validated_data.pop('season_id', None)
        if season_id is not None:
            validated_data['season_id'] = season_id
        return super().update(instance, validated_data)

class MissionProgressSerializer(serializers.ModelSerializer):
    """Serializer für Mission-Fortschritt"""
    mission = MissionSerializer(read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = MissionProgress
        fields = [
            'id', 'mission', 'current_value', 'is_completed', 'completed_at',
            'progress_percentage', 'is_expired', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_progress_percentage(self, obj):
        return obj.get_progress_percentage()
    
    def get_is_expired(self, obj):
        return obj.is_expired()

class ActiveMissionSerializer(serializers.ModelSerializer):
    """Serializer für aktive Missionen mit Fortschritt"""
    progress = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Mission
        fields = [
            'id', 'title', 'description', 'mission_type', 'unit', 'target_value',
            'xp_reward', 'gold_reward', 'ultra_point_reward',
            'start_time', 'end_time', 'progress', 'progress_percentage',
            'is_active', 'created_at'
        ]
    
    def get_progress(self, obj):
        user = self.context.get('request').user
        try:
            progress = obj.user_progress.get(user=user)
            return MissionProgressSerializer(progress).data
        except MissionProgress.DoesNotExist:
            return None
    
    def get_progress_percentage(self, obj):
        user = self.context.get('request').user
        try:
            progress = obj.user_progress.get(user=user)
            return progress.get_progress_percentage()
        except MissionProgress.DoesNotExist:
            return 0

class CompletedMissionSerializer(serializers.ModelSerializer):
    """Serializer für abgeschlossene Missionen"""
    mission = MissionSerializer(read_only=True)
    completion_time = serializers.SerializerMethodField()
    
    class Meta:
        model = MissionProgress
        fields = [
            'id', 'mission', 'current_value', 'completed_at', 'completion_time'
        ]
    
    def get_completion_time(self, obj):
        if obj.completed_at:
            return obj.completed_at.strftime("%Y-%m-%d %H:%M:%S")
        return None

class MissionCreateSerializer(serializers.ModelSerializer):
    """Serializer für das Erstellen neuer Missionen"""
    
    class Meta:
        model = Mission
        fields = [
            'title', 'description', 'mission_type', 'unit', 'target_value',
            'xp_reward', 'gold_reward', 'ultra_point_reward',
            'start_time', 'end_time', 'season', 'is_active'
        ]
    
    def validate(self, data):
        """Validiert die Mission-Daten"""
        mission_type = data.get('mission_type')
        season = data.get('season')
        
        # Saisonale Missionen müssen eine Season haben
        if mission_type == 'seasonal' and not season:
            raise serializers.ValidationError(
                "Saisonale Missionen müssen einer Season zugeordnet werden."
            )
        
        # Nicht-saisonale Missionen sollten keine Season haben
        if mission_type != 'seasonal' and season:
            raise serializers.ValidationError(
                "Nur saisonale Missionen können einer Season zugeordnet werden."
            )
        
        # Mindestens eine Belohnung sollte vorhanden sein
        rewards = [
            data.get('xp_reward', 0),
            data.get('gold_reward', 0),
            data.get('ultra_point_reward', 0)
        ]
        if not any(rewards):
            raise serializers.ValidationError(
                "Mindestens eine Belohnung muss gesetzt werden."
            )
        
        return data

class SeasonCreateSerializer(serializers.ModelSerializer):
    """Serializer für das Erstellen neuer Seasons"""
    
    class Meta:
        model = Season
        fields = [
            'title', 'description', 'start_date', 'end_date', 'is_active'
        ]
    
    def validate(self, data):
        """Validiert die Season-Daten"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        is_active = data.get('is_active', False)
        
        # Validiere Zeitrahmen
        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError(
                "Das Enddatum muss nach dem Startdatum liegen."
            )
        
        # Prüfe ob bereits eine aktive Season existiert
        if is_active:
            existing_active = Season.objects.filter(is_active=True)
            if self.instance:
                existing_active = existing_active.exclude(pk=self.instance.pk)
            
            if existing_active.exists():
                raise serializers.ValidationError(
                    "Es kann nur eine Season gleichzeitig aktiv sein."
                )
        
        return data

class MissionProgressUpdateSerializer(serializers.Serializer):
    """Serializer für das manuelle Aktualisieren des Mission-Fortschritts"""
    value = serializers.IntegerField(min_value=1, default=1)
    
    def update_progress(self, user, unit):
        """Aktualisiert den Fortschritt für alle passenden Missionen"""
        value = self.validated_data.get('value', 1)
        MissionProgress.update_progress_for_activity(user, unit, value)
        return {"message": f"Fortschritt für {unit} um {value} erhöht"}

class MissionRewardSerializer(serializers.Serializer):
    """Serializer für Mission-Belohnungen"""
    xp_reward = serializers.IntegerField(min_value=0)
    gold_reward = serializers.IntegerField(min_value=0)
    ultra_point_reward = serializers.IntegerField(min_value=0)
    total_value = serializers.SerializerMethodField()
    
    def get_total_value(self, obj):
        return obj.get('xp_reward', 0) + obj.get('gold_reward', 0) + obj.get('ultra_point_reward', 0) 