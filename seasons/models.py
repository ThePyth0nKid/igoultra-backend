from django.db import models
from django.conf import settings

class Season(models.Model):
    """
    Eine dreimonatige Season mit Name, Start/Ende und Aktiv-Flag.
    """
    name      = models.CharField(max_length=100)   # z.B. "Stärker als dein Schmerz"
    start     = models.DateField()                 # Season-Beginn
    end       = models.DateField()                 # Season-Ende (exklusiv)
    is_active = models.BooleanField(default=False) # Nur eine Season läuft zur Zeit

    def __str__(self):
        return f"{self.name} ({self.start} – {self.end})"


class SeasonXp(models.Model):
    """
    Aggregiert, wie viele XP jeder User in einer Season gesammelt hat.
    """
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    user   = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    xp     = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("season", "user")

    def __str__(self):
        return f"{self.user} – {self.season.name}: {self.xp} XP"
