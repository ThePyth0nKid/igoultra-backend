from django.db import models
from django.conf import settings

# Create your models here.

class Layer(models.Model):
    LAYER_TYPE_CHOICES = [
        ('real', 'Realitäts-Layer'),
        ('cyber', 'Cyber-Layer'),
    ]
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=LAYER_TYPE_CHOICES)
    order = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    essence = models.CharField(max_length=200, blank=True)
    player_action = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.code} – {self.name}"

class UserLayerProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    real_layer = models.ForeignKey(
        Layer, on_delete=models.PROTECT, related_name='real_layer_progress',
        limit_choices_to={'type': 'real'}
    )
    cyber_layer = models.ForeignKey(
        Layer, on_delete=models.PROTECT, related_name='cyber_layer_progress',
        limit_choices_to={'type': 'cyber'}
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} RL:{self.real_layer} CL:{self.cyber_layer}"
