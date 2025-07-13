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

class SkillSerializer(serializers.ModelSerializer):
    """Serializer für Skills"""
    
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'description', 'layer', 'category', 'tier',
            'required_level', 'required_xp_type', 'required_xp_amount', 'required_stats',
            'effects', 'is_active', 'created_at'
        ]

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