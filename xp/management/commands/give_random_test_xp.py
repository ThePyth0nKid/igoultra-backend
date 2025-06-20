import random
from django.core.management.base import BaseCommand
from datetime import date, timedelta

from users.models import User
from xp.models import XpType, XpEvent
from seasons.models import Season, SeasonXp
from xp.services import add_xp_to_user

LAYER_CHOICES = ["Real-Life", "Cyber", "Game"]

class Command(BaseCommand):
    help = "Sorgt für saubere Test-Season + verteilt randomisierte XP an Test-User (6 Runden)."

    def handle(self, *args, **options):
        today = date.today()

        # 1️⃣ Deaktiviere alle Seasons
        Season.objects.filter(is_active=True).update(is_active=False)
        self.stdout.write(self.style.WARNING("❌ Alle bestehenden aktiven Seasons deaktiviert."))

        # 2️⃣ Test-Season finden oder erstellen
        season, created = Season.objects.get_or_create(
            name="Test-Season",
            defaults={
                "start": today - timedelta(days=7),
                "end": today + timedelta(days=30),
                "is_active": True
            }
        )
        if not created:
            season.is_active = True
            season.start = today - timedelta(days=7)
            season.end = today + timedelta(days=30)
            season.save()
            self.stdout.write(self.style.SUCCESS("✅ Test-Season reaktiviert und Zeitspanne aktualisiert."))
        else:
            self.stdout.write(self.style.SUCCESS("✅ Test-Season neu erstellt und aktiviert."))

        # 3️⃣ XpType sicherstellen
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

        # 4️⃣ Test-User sicherstellen
        test_users = list(User.objects.filter(username__startswith="testuser"))
        if not test_users:
            for i in range(1, 11):
                user = User.objects.create(username=f"testuser{i}", ultra_name=f"UltraTester{i}")
                test_users.append(user)
                self.stdout.write(self.style.SUCCESS(f"✅ Test-User '{user.username}' erstellt."))
        else:
            self.stdout.write(self.style.SUCCESS(f"✅ {len(test_users)} Test-User gefunden."))

        # 5️⃣ XP randomisiert vergeben
        for iteration in range(6):
            self.stdout.write(self.style.WARNING(f"\n🚀 Iteration {iteration + 1}"))
            for user in test_users:
                pushups = random.randint(5, 30)
                layer_type = random.choice(LAYER_CHOICES)

                result = add_xp_to_user(user, "pushups", amount_units=pushups, layer_type=layer_type)

                self.stdout.write(f"User: {user.username}, Layer: {layer_type}, Push-Ups: {pushups}, Awarded XP: {result['awarded_xp']}, Level: {result['level']}")

        # 6️⃣ SeasonXp anzeigen
        self.stdout.write(self.style.SUCCESS("\n✅ Finaler SeasonXp-Stand:"))
        for sxp in SeasonXp.objects.filter(season=season):
            self.stdout.write(f"  {sxp}")
