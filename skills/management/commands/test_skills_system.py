from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from skills.models import CharacterStats, Skill, UserSkill
from skills.services import get_user_stats, get_available_skills, unlock_skill
from xp.services import add_xp_to_user

User = get_user_model()

class Command(BaseCommand):
    help = "Testet das Skills- und XP-System"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🎮 Testing iGoUltra Skills System..."))
        
        # Test-User erstellen oder finden
        user, created = User.objects.get_or_create(
            username="test_skills_user",
            defaults={
                "email": "test@skills.com",
                "ultra_name": "SkillTester",
                "xp": 0,
                "level": 1
            }
        )
        
        if created:
            self.stdout.write(f"✅ Test-User erstellt: {user.username}")
        else:
            self.stdout.write(f"✅ Test-User gefunden: {user.username}")
        
        # Character Stats erstellen
        stats, created = CharacterStats.objects.get_or_create(user=user)
        if created:
            self.stdout.write("✅ Character Stats erstellt")
        else:
            self.stdout.write("✅ Character Stats gefunden")
        
        # Aktuelle Stats anzeigen
        current_stats = get_user_stats(user)
        self.stdout.write("\n📊 Aktuelle Stats:")
        for category, category_stats in current_stats.items():
            self.stdout.write(f"  {category}: {category_stats}")
        
        # XP hinzufügen (Physical)
        self.stdout.write("\n💪 Füge Physical XP hinzu...")
        result = add_xp_to_user(
            user=user,
            type_key="pushup_standard",
            amount_units=50,  # 50 Push-ups
            layer_type="Real-Life"
        )
        self.stdout.write(f"✅ {result['awarded_xp']} XP hinzugefügt")
        self.stdout.write(f"   Level: {result['level']} (Leveled up: {result['leveled_up']})")
        
        # Stats nach XP-Update
        updated_stats = get_user_stats(user)
        self.stdout.write("\n📊 Stats nach Physical XP:")
        for category, category_stats in updated_stats.items():
            self.stdout.write(f"  {category}: {category_stats}")
        
        # Mental XP hinzufügen
        self.stdout.write("\n🧠 Füge Mental XP hinzu...")
        result = add_xp_to_user(
            user=user,
            type_key="meditation_10min",
            amount_units=1,  # 1 Meditation Session
            layer_type="Real-Life"
        )
        self.stdout.write(f"✅ {result['awarded_xp']} XP hinzugefügt")
        
        # Verfügbare Skills anzeigen
        self.stdout.write("\n🎯 Verfügbare Skills:")
        available_skills = get_available_skills(user)
        
        for skill_info in available_skills:
            skill = skill_info['skill']
            can_unlock = skill_info['can_unlock']
            is_unlocked = skill_info['is_unlocked']
            message = skill_info['message']
            
            status = "🔓 Freigeschaltet" if is_unlocked else "✅ Verfügbar" if can_unlock else "❌ Nicht verfügbar"
            self.stdout.write(f"  {skill.name} ({skill.layer}) - {status}")
            if not can_unlock and not is_unlocked:
                self.stdout.write(f"    Grund: {message}")
        
        # Skill freischalten (falls möglich)
        unlockable_skills = [s for s in available_skills if s['can_unlock'] and not s['is_unlocked']]
        if unlockable_skills:
            skill_to_unlock = unlockable_skills[0]
            self.stdout.write(f"\n🔓 Versuche Skill freizuschalten: {skill_to_unlock['skill'].name}")
            success, message = unlock_skill(user, skill_to_unlock['skill'].id)
            if success:
                self.stdout.write(self.style.SUCCESS(f"✅ {message}"))
            else:
                self.stdout.write(self.style.ERROR(f"❌ {message}"))
        else:
            self.stdout.write("\n⚠️  Keine Skills zum Freischalten verfügbar")
        
        # Freigeschaltete Skills anzeigen
        self.stdout.write("\n🎉 Freigeschaltete Skills:")
        unlocked_skills = UserSkill.objects.filter(user=user, is_active=True).select_related('skill')
        if unlocked_skills:
            for user_skill in unlocked_skills:
                self.stdout.write(f"  ✅ {user_skill.skill.name} (freigeschaltet: {user_skill.unlocked_at.strftime('%Y-%m-%d %H:%M')})")
        else:
            self.stdout.write("  Keine Skills freigeschaltet")
        
        self.stdout.write(self.style.SUCCESS("\n🎮 Skills-System Test abgeschlossen!")) 