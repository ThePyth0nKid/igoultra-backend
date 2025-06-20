from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = "Erstellt 10 Test-User"

    def handle(self, *args, **kwargs):
        for i in range(1, 11):
            user, created = User.objects.get_or_create(
                username=f"testuser{i}",
                defaults={
                    "ultra_name": f"UltraTester{i}",
                    "discord_id": f"testdiscord{i}",
                    "xp": 0,
                    "level": 1,
                    "rank": "Unranked"
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created {user.username}"))
            else:
                self.stdout.write(f"Skipped {user.username} (already exists)")