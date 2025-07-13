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

# Skill-Typen für aktive/passive Unterscheidung
SKILL_TYPE_CHOICES = [
    ('active', 'Active'),
    ('passive', 'Passive'),
]

# Effekt-Typen für aktive Skills
EFFECT_TYPE_CHOICES = [
    ('stun', 'Stun'),
    ('burn', 'Burn'),
    ('slow', 'Slow'),
    ('heal', 'Heal'),
    ('damage', 'Damage'),
    ('buff', 'Buff'),
    ('debuff', 'Debuff'),
    ('teleport', 'Teleport'),
    ('shield', 'Shield'),
    ('stealth', 'Stealth'),
]

# Buff-Typen für passive Skills
BUFF_TYPE_CHOICES = [
    ('resistance', 'Resistance'),
    ('shield', 'Shield'),
    ('aura', 'Aura'),
    ('regeneration', 'Regeneration'),
    ('damage_boost', 'Damage Boost'),
    ('speed_boost', 'Speed Boost'),
    ('critical_chance', 'Critical Chance'),
    ('armor', 'Armor'),
    ('evasion', 'Evasion'),
    ('healing', 'Healing'),
]

# Trigger-Bedingungen für passive Skills
TRIGGER_CONDITION_CHOICES = [
    ('always_active', 'Always Active'),
    ('on_low_hp', 'On Low HP'),
    ('on_critical_hit', 'On Critical Hit'),
    ('on_damage_taken', 'On Damage Taken'),
    ('on_kill', 'On Kill'),
    ('on_heal', 'On Heal'),
    ('on_skill_use', 'On Skill Use'),
    ('on_block', 'On Block'),
    ('on_dodge', 'On Dodge'),
    ('on_combo', 'On Combo'),
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
    Unterstützt aktive und passive Skills mit unterschiedlichen Eigenschaften.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    layer = models.CharField(max_length=10, choices=LAYER_CHOICES)
    
    # Skill-Typ: aktiv oder passiv
    skill_type = models.CharField(
        max_length=10, 
        choices=SKILL_TYPE_CHOICES,
        default='active',
        help_text="Bestimmt ob der Skill aktiv oder passiv ist"
    )
    
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
    
    # === AKTIVE SKILL FELDER ===
    # Nur relevant wenn skill_type = 'active'
    range = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        help_text="Reichweite in Metern (nur für aktive Skills)"
    )
    area_of_effect = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        help_text="Radius der Wirkung in Metern (nur für aktive Skills)"
    )
    damage = models.IntegerField(
        blank=True, 
        null=True, 
        help_text="Schadenswert (positiv für Schaden, negativ für Heilung, nur für aktive Skills)"
    )
    duration = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        help_text="Dauer in Sekunden (nur für aktive Skills)"
    )
    effect_type = models.CharField(
        max_length=20, 
        choices=EFFECT_TYPE_CHOICES,
        blank=True, 
        null=True,
        help_text="Art des Effekts (nur für aktive Skills)"
    )
    
    # === PASSIVE SKILL FELDER ===
    # Nur relevant wenn skill_type = 'passive'
    buff_type = models.CharField(
        max_length=20, 
        choices=BUFF_TYPE_CHOICES,
        blank=True, 
        null=True,
        help_text="Art des Buffs (nur für passive Skills)"
    )
    buff_value = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="Buff-Wert z.B. '+10%', '+5', '2x' (nur für passive Skills)"
    )
    trigger_condition = models.CharField(
        max_length=20, 
        choices=TRIGGER_CONDITION_CHOICES,
        blank=True, 
        null=True,
        help_text="Aktivierungsbedingung (nur für passive Skills)"
    )
    passive_duration = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        help_text="Dauer in Sekunden (nur für temporäre passive Skills)"
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['skill_type', 'tier', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_skill_type_display()}, {self.layer})"
    
    def clean(self):
        """Validiert die Skill-Konfiguration basierend auf dem Skill-Typ"""
        from django.core.exceptions import ValidationError
        
        if self.skill_type == 'active':
            # Aktive Skills müssen mindestens einen Effekt haben
            if not any([self.damage, self.effect_type]):
                raise ValidationError("Aktive Skills müssen mindestens Schaden oder einen Effekt-Typ haben.")
            
            # Aktive Skills sollten eine Reichweite haben
            if not self.range:
                raise ValidationError("Aktive Skills sollten eine Reichweite haben.")
        
        elif self.skill_type == 'passive':
            # Passive Skills müssen einen Buff-Typ haben
            if not self.buff_type:
                raise ValidationError("Passive Skills müssen einen Buff-Typ haben.")
            
            # Passive Skills sollten einen Buff-Wert haben
            if not self.buff_value:
                raise ValidationError("Passive Skills müssen einen Buff-Wert haben.")
    
    def get_active_skill_data(self):
        """Gibt die aktiven Skill-Daten zurück"""
        if self.skill_type != 'active':
            return None
        
        return {
            'range': self.range,
            'area_of_effect': self.area_of_effect,
            'damage': self.damage,
            'duration': self.duration,
            'effect_type': self.effect_type,
        }
    
    def get_passive_skill_data(self):
        """Gibt die passiven Skill-Daten zurück"""
        if self.skill_type != 'passive':
            return None
        
        return {
            'buff_type': self.buff_type,
            'buff_value': self.buff_value,
            'trigger_condition': self.trigger_condition,
            'duration': self.passive_duration,
        }
    
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
