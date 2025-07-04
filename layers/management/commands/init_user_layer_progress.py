from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from layers.models import Layer, UserLayerProgress

class Command(BaseCommand):
    help = "Initialisiert UserLayerProgress für alle User, die noch keinen haben (RL0 und CL0)."

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            base_real = Layer.objects.get(code='RL0')
            base_cyber = Layer.objects.get(code='CL0')
        except Layer.DoesNotExist:
            self.stderr.write(self.style.ERROR('RL0 oder CL0 Layer fehlt!'))
            return
        created = 0
        for user in User.objects.all():
            if not UserLayerProgress.objects.filter(user=user).exists():
                UserLayerProgress.objects.create(
                    user=user,
                    real_layer=base_real,
                    cyber_layer=base_cyber
                )
                created += 1
        self.stdout.write(self.style.SUCCESS(f"{created} UserLayerProgress-Einträge erstellt.")) 