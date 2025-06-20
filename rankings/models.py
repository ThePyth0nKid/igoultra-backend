from django.db import models
from seasons.models import Season
from django.conf import settings

LAYER_TYPE_CHOICES = [
    ('Real-Life', 'Real-Life'),
    ('Cyber', 'Cyber'),
    ('Game', 'Game'),
]

class LayerRankingEntry(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    xp = models.PositiveIntegerField()
    layer_type = models.CharField(
        max_length=20,
        choices=LAYER_TYPE_CHOICES,
        default='Real-Life',  # Hier ist der Default gesetzt
        help_text="Layer, für den dieses Ranking gilt"
    )

    class Meta:
        ordering = ["-xp"]
        unique_together = ("season", "user", "layer_type")

    def __str__(self):
        return f"{self.user} – {self.season.name} [{self.layer_type}]: {self.xp} XP"
