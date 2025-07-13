from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

# Mission-Typen
MISSION_TYPE_CHOICES = [
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('seasonal', 'Seasonal'),
]

# Einheiten für Missionen
UNIT_CHOICES = [
    ('steps', 'Steps'),
    ('minutes_in_game', 'Minutes in Game'),
    ('pushups', 'Pushups'),
    ('quests_completed', 'Quests Completed'),
    ('xp_gained', 'XP Gained'),
    ('skills_unlocked', 'Skills Unlocked'),
    ('layers_completed', 'Layers Completed'),
    ('social_interactions', 'Social Interactions'),
    ('workout_sessions', 'Workout Sessions'),
    ('meditation_minutes', 'Meditation Minutes'),
    ('hacking_attempts', 'Hacking Attempts'),
    ('cyber_quests', 'Cyber Quests'),
    ('real_world_activities', 'Real World Activities'),
]

class Season(models.Model):
    """
    Saison für saisonale Missionen.
    Es darf nur eine aktive Season gleichzeitig existieren.
    """
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = "Season"
        verbose_name_plural = "Seasons"
    
    def __str__(self):
        return f"{self.title} ({'Active' if self.is_active else 'Inactive'})"
    
    def clean(self):
        """Validiert, dass nur eine Season gleichzeitig aktiv sein kann"""
        if self.is_active:
            # Prüfe ob bereits eine andere Season aktiv ist
            active_seasons = Season.objects.filter(is_active=True)
            if self.pk:
                active_seasons = active_seasons.exclude(pk=self.pk)
            
            if active_seasons.exists():
                raise ValidationError(
                    "Es kann nur eine Season gleichzeitig aktiv sein. "
                    "Deaktiviere zuerst die andere aktive Season."
                )
        
        # Validiere, dass end_date nach start_date liegt
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError("Das Enddatum muss nach dem Startdatum liegen.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    @classmethod
    def get_active_season(cls):
        """Gibt die aktuell aktive Season zurück"""
        return cls.objects.filter(is_active=True).first()
    
    def is_currently_active(self):
        """Prüft, ob die Season aktuell läuft"""
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

class Mission(models.Model):
    """
    Missionen für User (Daily, Weekly, Seasonal).
    Unterstützt verschiedene Einheiten und Belohnungen.
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    mission_type = models.CharField(max_length=20, choices=MISSION_TYPE_CHOICES)
    unit = models.CharField(max_length=30, choices=UNIT_CHOICES)
    target_value = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Zielwert für die Mission"
    )
    
    # Belohnungen
    xp_reward = models.PositiveIntegerField(default=0, help_text="XP-Belohnung")
    gold_reward = models.PositiveIntegerField(default=0, help_text="Gold-Belohnung")
    ultra_point_reward = models.PositiveIntegerField(default=0, help_text="Ultra-Point-Belohnung")
    
    # Zeitliche Begrenzung
    start_time = models.DateTimeField(blank=True, null=True, help_text="Startzeit der Mission")
    end_time = models.DateTimeField(blank=True, null=True, help_text="Endzeit der Mission")
    
    # Saisonale Missionen
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="Season für saisonale Missionen"
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['mission_type', 'created_at']
        verbose_name = "Mission"
        verbose_name_plural = "Missions"
    
    def __str__(self):
        return f"{self.title} ({self.get_mission_type_display()})"
    
    def clean(self):
        """Validiert die Mission-Konfiguration"""
        # Saisonale Missionen müssen eine Season haben
        if self.mission_type == 'seasonal' and not self.season:
            raise ValidationError("Saisonale Missionen müssen einer Season zugeordnet werden.")
        
        # Nicht-saisonale Missionen sollten keine Season haben
        if self.mission_type != 'seasonal' and self.season:
            raise ValidationError("Nur saisonale Missionen können einer Season zugeordnet werden.")
        
        # Validiere Zeitrahmen
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("Das Enddatum muss nach dem Startdatum liegen.")
        
        # Mindestens eine Belohnung sollte vorhanden sein
        if not any([self.xp_reward, self.gold_reward, self.ultra_point_reward]):
            raise ValidationError("Mindestens eine Belohnung muss gesetzt werden.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def is_currently_active(self):
        """Prüft, ob die Mission aktuell aktiv ist"""
        now = timezone.now()
        
        # Prüfe ob Mission aktiv ist
        if not self.is_active:
            return False
        
        # Prüfe Zeitrahmen falls gesetzt
        if self.start_time and now < self.start_time:
            return False
        if self.end_time and now > self.end_time:
            return False
        
        # Prüfe Season falls saisonal
        if self.mission_type == 'seasonal' and self.season:
            return self.season.is_currently_active()
        
        return True
    
    def get_active_missions_for_user(self, user):
        """Gibt alle aktiven Missionen für einen User zurück"""
        return MissionProgress.objects.filter(
            user=user,
            mission=self,
            is_completed=False
        )
    
    @classmethod
    def get_daily_missions(cls):
        """Gibt alle aktiven Daily-Missionen zurück"""
        return cls.objects.filter(
            mission_type='daily',
            is_active=True
        )
    
    @classmethod
    def get_weekly_missions(cls):
        """Gibt alle aktiven Weekly-Missionen zurück"""
        return cls.objects.filter(
            mission_type='weekly',
            is_active=True
        )
    
    @classmethod
    def get_seasonal_missions(cls):
        """Gibt alle aktiven Seasonal-Missionen zurück"""
        active_season = Season.get_active_season()
        if not active_season:
            return cls.objects.none()
        
        return cls.objects.filter(
            mission_type='seasonal',
            season=active_season,
            is_active=True
        )

class MissionProgress(models.Model):
    """
    Fortschritt eines Users bei einer Mission.
    Wird automatisch aktualisiert und validiert.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mission_progress'
    )
    mission = models.ForeignKey(
        Mission,
        on_delete=models.CASCADE,
        related_name='user_progress'
    )
    current_value = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'mission']
        ordering = ['-updated_at']
        verbose_name = "Mission Progress"
        verbose_name_plural = "Mission Progress"
    
    def __str__(self):
        status = "Completed" if self.is_completed else "In Progress"
        return f"{self.user.username} - {self.mission.title} ({status})"
    
    def clean(self):
        """Validiert den Fortschritt"""
        if self.current_value > self.mission.target_value:
            raise ValidationError("Der Fortschritt kann nicht höher als der Zielwert sein.")
        
        if self.is_completed and not self.completed_at:
            raise ValidationError("Abgeschlossene Missionen müssen einen completed_at Zeitstempel haben.")
    
    def save(self, *args, **kwargs):
        # Prüfe ob Mission abgeschlossen wurde
        if not self.is_completed and self.current_value >= self.mission.target_value:
            self.is_completed = True
            self.completed_at = timezone.now()
        
        self.clean()
        super().save(*args, **kwargs)
    
    def increment_progress(self, value=1):
        """Erhöht den Fortschritt um den angegebenen Wert, aber maximal bis target_value"""
        if not self.is_completed:
            max_increment = self.mission.target_value - self.current_value
            if value > max_increment:
                value = max_increment
            if value > 0:
                self.current_value += value
                self.save()
    
    def get_progress_percentage(self):
        """Gibt den Fortschritt in Prozent zurück"""
        if self.mission.target_value == 0:
            return 0
        return min(100, (self.current_value / self.mission.target_value) * 100)
    
    def is_expired(self):
        """Prüft, ob die Mission abgelaufen ist"""
        if not self.mission.is_currently_active():
            return True
        
        # Prüfe spezifische Endzeit
        if self.mission.end_time and timezone.now() > self.mission.end_time:
            return True
        
        return False
    
    @classmethod
    def create_progress_for_user(cls, user, mission):
        """Erstellt einen neuen Fortschritt für einen User und eine Mission"""
        progress, created = cls.objects.get_or_create(
            user=user,
            mission=mission,
            defaults={'current_value': 0}
        )
        return progress
    
    @classmethod
    def update_progress_for_activity(cls, user, unit, value=1):
        """
        Aktualisiert den Fortschritt für alle passenden Missionen basierend auf einer Aktivität.
        Wird automatisch aufgerufen, wenn User Aktivitäten durchführen.
        """
        # Finde alle aktiven Missionen mit der passenden Einheit
        active_missions = Mission.objects.filter(
            unit=unit,
            is_active=True
        ).filter(
            models.Q(start_time__isnull=True) | models.Q(start_time__lte=timezone.now())
        ).filter(
            models.Q(end_time__isnull=True) | models.Q(end_time__gte=timezone.now())
        )
        
        # Prüfe saisonale Missionen
        if unit in ['seasonal_quests', 'seasonal_activities']:
            active_season = Season.get_active_season()
            if active_season:
                seasonal_missions = Mission.objects.filter(
                    mission_type='seasonal',
                    season=active_season,
                    is_active=True
                )
                active_missions = active_missions.union(seasonal_missions)
        
        # Aktualisiere Fortschritt für jede passende Mission
        for mission in active_missions:
            if mission.is_currently_active():
                progress = cls.create_progress_for_user(user, mission)
                progress.increment_progress(value)
