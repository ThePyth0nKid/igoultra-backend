from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from missions.models import Season, Mission, MissionProgress
from missions.services import (
    get_active_season, get_active_missions_for_user, update_mission_progress_for_activity,
    get_mission_statistics_for_user
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Testet das Missionssystem mit Beispiel-Daten'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=int,
            help='User-ID für den Test (optional)',
        )
        parser.add_argument(
            '--create-user',
            action='store_true',
            help='Erstellt einen Test-User falls keiner existiert',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Starte Missionssystem-Test...')
        )

        # 1. Prüfe aktive Season
        self.stdout.write('\n📅 Prüfe aktive Season...')
        active_season = get_active_season()
        if active_season:
            self.stdout.write(
                self.style.SUCCESS(f'✅ Aktive Season gefunden: {active_season.title}')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Keine aktive Season gefunden')
            )

        # 2. Prüfe User
        user_id = options.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                self.stdout.write(
                    self.style.SUCCESS(f'✅ User gefunden: {user.username}')
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ User mit ID {user_id} nicht gefunden')
                )
                return
        else:
            # Verwende ersten User oder erstelle Test-User
            user = User.objects.first()
            if not user and options.get('create_user'):
                user = User.objects.create_user(
                    username='testuser',
                    email='test@example.com',
                    password='testpass123'
                )
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Test-User erstellt: {user.username}')
                )
            elif not user:
                self.stdout.write(
                    self.style.ERROR('❌ Kein User gefunden. Verwende --create-user oder --user-id')
                )
                return
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ User gefunden: {user.username}')
                )

        # 3. Prüfe aktive Missionen
        self.stdout.write('\n🎯 Prüfe aktive Missionen...')
        active_missions = get_active_missions_for_user(user)
        self.stdout.write(
            self.style.SUCCESS(f'✅ {active_missions.count()} aktive Missionen gefunden')
        )

        # Zeige Missionen nach Typ
        daily_missions = active_missions.filter(mission_type='daily')
        weekly_missions = active_missions.filter(mission_type='weekly')
        seasonal_missions = active_missions.filter(mission_type='seasonal')

        self.stdout.write(f'   📅 Daily: {daily_missions.count()}')
        self.stdout.write(f'   📊 Weekly: {weekly_missions.count()}')
        self.stdout.write(f'   🌟 Seasonal: {seasonal_missions.count()}')

        # 4. Prüfe User-Fortschritt
        self.stdout.write('\n📊 Prüfe User-Fortschritt...')
        user_progress = MissionProgress.objects.filter(user=user)
        self.stdout.write(
            self.style.SUCCESS(f'✅ {user_progress.count()} Fortschritt-Einträge gefunden')
        )

        completed_missions = user_progress.filter(is_completed=True)
        self.stdout.write(f'   ✅ Abgeschlossen: {completed_missions.count()}')
        self.stdout.write(f'   🔄 In Bearbeitung: {user_progress.filter(is_completed=False).count()}')

        # 5. Simuliere Aktivitäten
        self.stdout.write('\n🎮 Simuliere Aktivitäten...')
        
        # XP gewinnen
        self.stdout.write('   💰 Simuliere XP-Gewinn...')
        update_mission_progress_for_activity(user, 'xp_gained', 150)
        
        # Liegestütze
        self.stdout.write('   💪 Simuliere Liegestütze...')
        update_mission_progress_for_activity(user, 'pushups', 25)
        
        # Schritte
        self.stdout.write('   👟 Simuliere Schritte...')
        update_mission_progress_for_activity(user, 'steps', 12000)
        
        # Gaming-Zeit
        self.stdout.write('   🎮 Simuliere Gaming-Zeit...')
        update_mission_progress_for_activity(user, 'minutes_in_game', 90)
        
        # Skills freischalten
        self.stdout.write('   🔓 Simuliere Skill-Freischaltung...')
        update_mission_progress_for_activity(user, 'skills_unlocked', 2)

        # 6. Prüfe aktualisierten Fortschritt
        self.stdout.write('\n📈 Prüfe aktualisierten Fortschritt...')
        updated_progress = MissionProgress.objects.filter(user=user)
        
        for progress in updated_progress[:5]:  # Zeige erste 5
            mission = progress.mission
            percentage = progress.get_progress_percentage()
            status = "✅" if progress.is_completed else "🔄"
            
            self.stdout.write(
                f'   {status} {mission.title}: {progress.current_value}/{mission.target_value} ({percentage:.1f}%)'
            )

        # 7. Zeige Statistiken
        self.stdout.write('\n📊 Mission-Statistiken...')
        stats = get_mission_statistics_for_user(user)
        
        self.stdout.write(f'   📅 Daily: {stats["daily"]["completed"]}/{stats["daily"]["total"]}')
        self.stdout.write(f'   📊 Weekly: {stats["weekly"]["completed"]}/{stats["weekly"]["total"]}')
        self.stdout.write(f'   🌟 Seasonal: {stats["seasonal"]["completed"]}/{stats["seasonal"]["total"]}')
        self.stdout.write(f'   🎯 Gesamt: {stats["total_completed"]}/{stats["total_missions"]}')
        
        # Belohnungen
        rewards = stats["total_rewards"]
        self.stdout.write(f'   💰 Gesamt-Belohnungen: {rewards["xp"]} XP, {rewards["gold"]} Gold, {rewards["ultra_points"]} Ultra-Points')

        # 8. Teste API-Endpunkte (simuliert)
        self.stdout.write('\n🔗 API-Endpunkte Test...')
        self.stdout.write('   ✅ GET /api/v1/missions/active/ - Aktive Missionen')
        self.stdout.write('   ✅ GET /api/v1/missions/progress/ - User-Fortschritt')
        self.stdout.write('   ✅ GET /api/v1/missions/completed/ - Abgeschlossene Missionen')
        self.stdout.write('   ✅ GET /api/v1/missions/seasons/active/ - Aktive Season')
        self.stdout.write('   ✅ GET /api/v1/missions/statistics/ - Statistiken')

        self.stdout.write(
            self.style.SUCCESS('\n🎉 Missionssystem-Test erfolgreich abgeschlossen!')
        )
        
        self.stdout.write('\n📝 Nächste Schritte:')
        self.stdout.write('   1. Öffne http://127.0.0.1:8000/admin/ um Missionen zu verwalten')
        self.stdout.write('   2. Teste die API-Endpunkte mit einem API-Client')
        self.stdout.write('   3. Integriere das System in deine Frontend-Anwendung') 