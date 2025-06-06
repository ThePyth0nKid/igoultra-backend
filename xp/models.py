from django.conf import settings
from django.db import models
from django.utils import timezone

class XpType(models.Model):
    """
    Definiert eine Aktivität, für die XP vergeben werden.
    """
    key = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=200)
    xp_amount = models.FloatField(
        help_text='XP pro Einheit (z. B. 5 XP/Repetition oder 2 XP/Minute)'
    )
    unit = models.CharField(
        max_length=50,
        help_text='z. B. "repetition", "time_minute", "step"'
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.display_name} ({self.xp_amount} XP/{self.unit})"


class XpEvent(models.Model):
    """
    Protokolliert jede XP-Änderung für einen User.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='xp_events'
    )
    amount = models.IntegerField(
        help_text='Positiv = Gain, Negativ = Abzug'
    )
    source = models.CharField(
        max_length=50,
        help_text='Identifier, z. B. "pushups", "running"'
    )
    metadata = models.JSONField(
        blank=True, null=True,
        help_text='z. B. {"unit":"time_minute","raw":"15 Minuten Yoga"}'
    )
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return f"{self.user}: {self.amount} XP via {self.source} at {self.timestamp}"
