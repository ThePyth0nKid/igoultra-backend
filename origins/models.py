from django.db import models

# Create your models here.

class Origin(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=50, blank=True, null=True, help_text='z.B. Ort, Land, Planet, etc.')

    def __str__(self):
        return self.name
