from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# XP-Typen für das erweiterte System
XP_TYPE_CHOICES = [
    ('Physical', 'Physical'),
    ('Mental', 'Mental'), 
    ('Cyber', 'Cyber'),
    ('Ultra', 'Ultra'),
]

# Stat-Kategorien
STAT_CATEGORY_CHOICES = [
    ('Body', 'Body'),
    ('Mind', 'Mind'),
    ('Spirit', 'Spirit'),
    ('Combat', 'Combat'),
    ('Tech', 'Tech'),
]

# Layer-Zuordnung für Skills
LAYER_CHOICES = [
    ('Real', 'Real'),
    ('Cyber', 'Cyber'),
]

class CharacterStats(models.Model):
    """
    Charakter-Statistiken für jeden User.
    Stats werden durch XP-Events automatisch erhöht.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='character_stats'
    )
    
    # Body Stats
    strength = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    endurance = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    agility = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    
    # Mind Stats
    intelligence = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    focus = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    memory = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    
    # Spirit Stats
    willpower = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    charisma = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    intuition = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    
    # Combat Stats
    combat_skill = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    reaction_time = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    tactical_awareness = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    
    # Tech Stats
    hacking = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    programming = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    cyber_awareness = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Character Stats"
        verbose_name_plural = "Character Stats"
    
    def __str__(self):
        return f"{self.user.username} Stats"
    
    def get_stat(self, stat_name):
        """Gibt den Wert einer bestimmten Stat zurück"""
        return getattr(self, stat_name, 1)
    
    def get_category_stats(self, category):
        """Gibt alle Stats einer Kategorie zurück"""
        category_mapping = {
            'Body': ['strength', 'endurance', 'agility'],
            'Mind': ['intelligence', 'focus', 'memory'],
            'Spirit': ['willpower', 'charisma', 'intuition'],
            'Combat': ['combat_skill', 'reaction_time', 'tactical_awareness'],
            'Tech': ['hacking', 'programming', 'cyber_awareness'],
        }
        stats = category_mapping.get(category, [])
        return {stat: self.get_stat(stat) for stat in stats}
    
    def get_all_stats(self):
        """Gibt alle Stats als Dictionary zurück"""
        return {
            'Body': self.get_category_stats('Body'),
            'Mind': self.get_category_stats('Mind'),
            'Spirit': self.get_category_stats('Spirit'),
            'Combat': self.get_category_stats('Combat'),
            'Tech': self.get_category_stats('Tech'),
        }

class Skill(models.Model):
    """
    Fähigkeiten, die durch bestimmte Voraussetzungen freigeschaltet werden können.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    layer = models.CharField(max_length=10, choices=LAYER_CHOICES)
    
    # Voraussetzungen
    required_level = models.PositiveIntegerField(default=1, help_text="Minimales Level")
    required_xp_type = models.CharField(max_length=20, choices=XP_TYPE_CHOICES, blank=True, null=True)
    required_xp_amount = models.PositiveIntegerField(default=0, help_text="Minimale XP in diesem Typ")
    
    # Stat-Voraussetzungen (JSON-Feld für Flexibilität)
    required_stats = models.JSONField(
        default=dict,
        help_text='{"strength": 10, "intelligence": 15}'
    )
    
    # Skill-Effekte (für zukünftige Erweiterungen)
    effects = models.JSONField(
        default=dict,
        help_text='Skill-Effekte und Boni'
    )
    
    # Skill-Kategorisierung
    category = models.CharField(max_length=50, blank=True, help_text="z.B. 'Combat', 'Utility'")
    tier = models.PositiveIntegerField(default=1, help_text="Skill-Tier (1-5)")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['tier', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.layer})"
    
    def check_requirements(self, user):
        """
        Prüft, ob ein User die Voraussetzungen für diesen Skill erfüllt.
        """
        # Level-Check
        if user.level < self.required_level:
            return False, f"Level {self.required_level} erforderlich (aktuell: {user.level})"
        
        # XP-Typ-Check
        if self.required_xp_type and self.required_xp_amount > 0:
            total_xp_in_type = user.xp_events.filter(
                source__startswith=self.required_xp_type.lower()
            ).aggregate(total=models.Sum('amount'))['total'] or 0
            
            if total_xp_in_type < self.required_xp_amount:
                return False, f"{self.required_xp_amount} {self.required_xp_type} XP erforderlich"
        
        # Stat-Check
        if self.required_stats:
            try:
                stats = user.character_stats
                for stat_name, required_value in self.required_stats.items():
                    current_value = stats.get_stat(stat_name)
                    if current_value < required_value:
                        return False, f"{stat_name}: {required_value} erforderlich (aktuell: {current_value})"
            except CharacterStats.DoesNotExist:
                return False, "Character Stats nicht gefunden"
        
        return True, "Alle Voraussetzungen erfüllt"

class UserSkill(models.Model):
    """
    Verknüpfung zwischen User und freigeschalteten Skills.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_skills'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='user_skills'
    )
    
    unlocked_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['user', 'skill']
        ordering = ['-unlocked_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.skill.name}"
