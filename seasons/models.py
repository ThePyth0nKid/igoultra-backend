from django.db import models
from django.conf import settings

LAYER_TYPE_CHOICES = [
    ('Real-Life', 'Real-Life'),
    ('Cyber', 'Cyber'),
    ('Game', 'Game'),
]

class Season(models.Model):
    """
    Eine Season mit Name, Start/Ende und Aktiv-Flag – layer-unabhängig.
    """
    name = models.CharField(max_length=100)   # z.B. "Stärker als dein Schmerz"
    start = models.DateField()                # Season-Beginn
    end = models.DateField()                  # Season-Ende (exklusiv)
    is_active = models.BooleanField(default=False)  # Nur eine Season läuft zur Zeit

    def __str__(self):
        return f"{self.name} ({self.start} – {self.end})"

class SeasonXp(models.Model):
    """
    Aggregiert, wie viele XP ein User in einer Season pro Layer gesammelt hat.
    """
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    layer_type = models.CharField(
        max_length=20,
        choices=LAYER_TYPE_CHOICES,
        default='Real-Life',  # Standardwert gesetzt
        help_text="Layer, für den diese XP gelten"
    )
    xp = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("season", "user", "layer_type")
        ordering = ["-xp"]

    def __str__(self):
        return f"{self.user} – {self.season.name} [{self.layer_type}]: {self.xp} XP"
