from rest_framework import serializers
from .models import CharacterStats, Skill, UserSkill
from .services import get_skill_progress

class CharacterStatsSerializer(serializers.ModelSerializer):
    """Serializer für CharacterStats"""
    
    class Meta:
        model = CharacterStats
        fields = [
            'strength', 'endurance', 'agility',
            'intelligence', 'focus', 'memory',
            'willpower', 'charisma', 'intuition',
            'combat_skill', 'reaction_time', 'tactical_awareness',
            'hacking', 'programming', 'cyber_awareness',
            'updated_at'
        ]
        read_only_fields = fields

class ActiveSkillSerializer(serializers.ModelSerializer):
    """Serializer für aktive Skills mit spezifischen Feldern"""
    
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'description', 'layer', 'category', 'tier',
            'skill_type', 'required_level', 'required_xp_type', 'required_xp_amount', 
            'required_stats', 'effects', 'is_active', 'created_at',
            # Aktive Skill spezifische Felder
            'range', 'area_of_effect', 'damage', 'duration', 'effect_type'
        ]
        read_only_fields = ['id', 'created_at']

class PassiveSkillSerializer(serializers.ModelSerializer):
    """Serializer für passive Skills mit spezifischen Feldern"""
    
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'description', 'layer', 'category', 'tier',
            'skill_type', 'required_level', 'required_xp_type', 'required_xp_amount', 
            'required_stats', 'effects', 'is_active', 'created_at',
            # Passive Skill spezifische Felder
            'buff_type', 'buff_value', 'trigger_condition', 'passive_duration'
        ]
        read_only_fields = ['id', 'created_at']

class SkillSerializer(serializers.ModelSerializer):
    """Erweiterter Serializer für Skills mit aktiven/passiven Daten"""
    
    # Dynamische Felder basierend auf Skill-Typ
    active_skill_data = serializers.SerializerMethodField()
    passive_skill_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'description', 'layer', 'category', 'tier',
            'skill_type', 'required_level', 'required_xp_type', 'required_xp_amount', 
            'required_stats', 'effects', 'is_active', 'created_at',
            'active_skill_data', 'passive_skill_data'
        ]
    
    def get_active_skill_data(self, obj):
        """Gibt aktive Skill-Daten zurück wenn skill_type = 'active'"""
        if obj.skill_type == 'active':
            return obj.get_active_skill_data()
        return None
    
    def get_passive_skill_data(self, obj):
        """Gibt passive Skill-Daten zurück wenn skill_type = 'passive'"""
        if obj.skill_type == 'passive':
            return obj.get_passive_skill_data()
        return None

class UserSkillSerializer(serializers.ModelSerializer):
    """Serializer für UserSkills mit Skill-Details"""
    skill = SkillSerializer(read_only=True)
    
    class Meta:
        model = UserSkill
        fields = ['id', 'skill', 'unlocked_at', 'is_active']

class SkillProgressSerializer(serializers.Serializer):
    """Serializer für Skill-Fortschritt"""
    skill = SkillSerializer()
    requirements_met = serializers.DictField()
    overall_progress = serializers.FloatField()
    can_unlock = serializers.BooleanField()
    message = serializers.CharField()
    is_unlocked = serializers.BooleanField()

class AvailableSkillSerializer(serializers.Serializer):
    """Serializer für verfügbare Skills"""
    skill = SkillSerializer()
    can_unlock = serializers.BooleanField()
    message = serializers.CharField()
    is_unlocked = serializers.BooleanField()

class UnlockSkillSerializer(serializers.Serializer):
    """Serializer für Skill-Freischaltung"""
    skill_id = serializers.IntegerField(help_text="ID des freizuschaltenden Skills")

class StatsOverviewSerializer(serializers.Serializer):
    """Serializer für Stats-Übersicht"""
    Body = serializers.DictField()
    Mind = serializers.DictField()
    Spirit = serializers.DictField()
    Combat = serializers.DictField()
    Tech = serializers.DictField()

class SkillCreateSerializer(serializers.ModelSerializer):
    """Serializer für das Erstellen neuer Skills mit Validierung"""
    
    class Meta:
        model = Skill
        fields = [
            'name', 'description', 'layer', 'category', 'tier',
            'skill_type', 'required_level', 'required_xp_type', 'required_xp_amount', 
            'required_stats', 'effects',
            # Aktive Skill Felder
            'range', 'area_of_effect', 'damage', 'duration', 'effect_type',
            # Passive Skill Felder
            'buff_type', 'buff_value', 'trigger_condition', 'passive_duration'
        ]
    
    def validate(self, data):
        """Validiert die Skill-Daten basierend auf dem Skill-Typ"""
        skill_type = data.get('skill_type', 'active')
        
        if skill_type == 'active':
            # Prüfe ob mindestens ein aktiver Skill Parameter vorhanden ist
            active_fields = ['damage', 'effect_type']
            if not any(data.get(field) for field in active_fields):
                raise serializers.ValidationError(
                    "Aktive Skills müssen mindestens Schaden oder einen Effekt-Typ haben."
                )
            
            # Prüfe ob Reichweite vorhanden ist
            if not data.get('range'):
                raise serializers.ValidationError(
                    "Aktive Skills müssen eine Reichweite haben."
                )
        
        elif skill_type == 'passive':
            # Prüfe ob Buff-Typ vorhanden ist
            if not data.get('buff_type'):
                raise serializers.ValidationError(
                    "Passive Skills müssen einen Buff-Typ haben."
                )
            
            # Prüfe ob Buff-Wert vorhanden ist
            if not data.get('buff_value'):
                raise serializers.ValidationError(
                    "Passive Skills müssen einen Buff-Wert haben."
                )
        
        return data
    
    def to_representation(self, instance):
        """Gibt die Daten in der korrekten Form zurück"""
        # Verwende den passenden Serializer basierend auf dem Skill-Typ
        if instance.skill_type == 'active':
            return ActiveSkillSerializer(instance).data
        elif instance.skill_type == 'passive':
            return PassiveSkillSerializer(instance).data
        else:
            return SkillSerializer(instance).data 