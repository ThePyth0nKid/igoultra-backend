from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta

from users.models import User
from xp.models import XpType, XpEvent
from seasons.models import Season, SeasonXp
from xp.services import add_xp_to_user

class Command(BaseCommand):
    help = "Gibt Test-XP an einen Test-User für Real-Life Layer und zeigt Status an."

    def handle(self, *args, **options):
        # 1️⃣ XpType sicherstellen
        xp_type, _ = XpType.objects.get_or_create(
            key="pushups",
            defaults={
                "display_name": "Push-Ups",
                "xp_amount": 5,
                "unit": "repetition",
                "description": "Klassische Push-Ups"
            }
        )
        self.stdout.write(self.style.SUCCESS(f"✅ XpType '{xp_type.display_name}' bereit."))

        # 2️⃣ Season sicherstellen
        today = date.today()
        season, _ = Season.objects.get_or_create(
            name="Test-Season",
            defaults={
                "start": today - timedelta(days=7),
                "end": today + timedelta(days=30),
                "is_active": True
            }
        )
        self.stdout.write(self.style.SUCCESS(f"✅ Season '{season.name}' aktiv."))

        # 3️⃣ Test-User sicherstellen
        user = User.objects.filter(username__startswith="testuser").first()
        if not user:
            user = User.objects.create(username="testuser1", ultra_name="UltraTester1")
            self.stdout.write(self.style.SUCCESS(f"✅ Test-User '{user.username}' erstellt."))
        else:
            self.stdout.write(self.style.SUCCESS(f"✅ Test-User '{user.username}' gefunden."))

        # 4️⃣ XP vergeben
        result = add_xp_to_user(user, "pushups", amount_units=10, layer_type="Real-Life")

        self.stdout.write("\n✅ Ergebnis:")
        for k, v in result.items():
            self.stdout.write(f"  {k}: {v}")

        # 5️⃣ Kontrolle SeasonXp + XpEvent
        self.stdout.write("\n✅ SeasonXp:")
        for sxp in SeasonXp.objects.filter(user=user):
            self.stdout.write(f"  {sxp}")

        self.stdout.write("\n✅ XpEvents:")
        for xe in XpEvent.objects.filter(user=user):
            self.stdout.write(f"  {xe}")
