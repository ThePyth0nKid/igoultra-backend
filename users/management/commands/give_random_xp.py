from django.core.management.base import BaseCommand
from users.models import User
from xp.models import XpEvent
from random import randint, choice
from datetime import datetime

LAYER_TYPE_CHOICES = ['Real-Life', 'Cyber', 'Game']

class Command(BaseCommand):
    help = "Gibt allen Test-Usern zufällige, realistische XP"

    def handle(self, *args, **kwargs):
        users = User.objects.filter(username__startswith="testuser")
        for user in users:
            # Z.B. 100 bis 5000 XP, um realistische Unterschiede zu erzeugen
            random_xp = randint(100, 5000)
            layer_type = choice(LAYER_TYPE_CHOICES)

            # XpEvent erstellen (optional, falls du XP-Verlauf trackst)
            XpEvent.objects.create(
                user=user,
                amount=random_xp,
                source="test_xp_generator",
                metadata={"layer_type": layer_type, "note": "Testdata XP"},
                timestamp=datetime.now()
            )

            # XP direkt auf User addieren (oder über dein XP-System summieren)
            user.xp += random_xp
            user.save()

            self.stdout.write(self.style.SUCCESS(
                f"{user.username} bekam {random_xp} XP im Layer {layer_type}"
            ))
