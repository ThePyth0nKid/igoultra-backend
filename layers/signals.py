from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from layers.models import Layer, UserLayerProgress

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_layer_progress(sender, instance, created, **kwargs):
    if created:
        try:
            base_real = Layer.objects.get(code='RL0')
            base_cyber = Layer.objects.get(code='CL0')
            UserLayerProgress.objects.create(
                user=instance,
                real_layer=base_real,
                cyber_layer=base_cyber
            )
        except Layer.DoesNotExist:
            pass 