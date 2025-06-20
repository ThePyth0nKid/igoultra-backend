from django.db import models
from django.conf import settings

LAYER_TYPE_CHOICES = [
    ('Real-Life', 'Real-Life'),
    ('Cyber', 'Cyber'),
    ('Game', 'Game'),
]

class Season(models.Model):
    name = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.start} – {self.end})"

class SeasonXp(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    layer_type = models.CharField(
        max_length=20,
        choices=LAYER_TYPE_CHOICES,
        default='Real-Life',
        help_text="Layer, für den diese Season XP gelten"
    )
    xp = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("season", "user", "layer_type")
        ordering = ["-xp"]

    def __str__(self):
        return f"{self.user} – {self.season.name} [{self.layer_type}]: {self.xp} XP"
