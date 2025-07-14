from django.db import models

# Create your models here.

class Faction(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    style = models.CharField(max_length=50, blank=True, null=True, help_text='Optionaler Style/Theme-Name')
    icon = models.URLField(blank=True, null=True, help_text='Optionales Icon (URL)')

    def __str__(self):
        return self.name
