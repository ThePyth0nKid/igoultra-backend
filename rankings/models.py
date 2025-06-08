# rankings/models.py

from django.db import models
from seasons.models import Season
from django.conf import settings
from rankings.constants import REAL_LAYERS, CYBER_LAYERS

class LayerRankingEntry(models.Model):
    season      = models.ForeignKey(Season, on_delete=models.CASCADE)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    real_layer  = models.CharField(
        max_length=20,
        choices=[(l, l) for l in REAL_LAYERS],
        default=REAL_LAYERS[0],          # Default BaseLayer
        help_text="Snapshot Realitäts-Layer am Season-Ende",
    )
    cyber_layer = models.CharField(
        max_length=20,
        choices=[(l, l) for l in CYBER_LAYERS],
        default=CYBER_LAYERS[0],         # Default SurfaceWebLayer
        help_text="Snapshot Cyber-Layer am Season-Ende",
    )
    xp          = models.PositiveIntegerField()

    class Meta:
        ordering = ["-xp"]
