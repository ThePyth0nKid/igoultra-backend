# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the User model.
    """
    model = User
    list_display = (
        "username",
        "ultra_name",
        "discord_id",
        "xp",
        "level",
        "rank",
        "real_layer",
        "cyber_layer",
        "character_stats_link",
        "is_staff",
    )

    fieldsets = UserAdmin.fieldsets + (
        ("Ultra Profile", {
            "fields": (
                "ultra_name",
                "discord_id",
                "xp",
                "level",
                "rank",
                "real_layer",
                "cyber_layer",
                "avatar_url",
            )
        }),
        ("Character Stats", {
            "fields": ("character_stats_display",),
            "classes": ("collapse",)
        }),
    )
    
    readonly_fields = ("character_stats_display", "character_stats_link")
    
    def character_stats_link(self, obj):
        """Link zu den Character Stats"""
        try:
            stats = obj.character_stats
            url = reverse('admin:skills_characterstats_change', args=[stats.id])
            return format_html('<a href="{}">Stats anzeigen</a>', url)
        except:
            return "Keine Stats"
    character_stats_link.short_description = "Character Stats"
    
    def character_stats_display(self, obj):
        """Zeigt die Character Stats direkt in der User-Detail-Ansicht"""
        try:
            stats = obj.character_stats
            html = f"""
            <div style="background: #f9f9f9; padding: 10px; border-radius: 5px;">
                <h3>Character Stats für {obj.username}</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div>
                        <h4>Body Stats</h4>
                        <p><strong>Strength:</strong> {stats.strength}</p>
                        <p><strong>Endurance:</strong> {stats.endurance}</p>
                        <p><strong>Agility:</strong> {stats.agility}</p>
                    </div>
                    <div>
                        <h4>Mind Stats</h4>
                        <p><strong>Intelligence:</strong> {stats.intelligence}</p>
                        <p><strong>Focus:</strong> {stats.focus}</p>
                        <p><strong>Memory:</strong> {stats.memory}</p>
                    </div>
                    <div>
                        <h4>Spirit Stats</h4>
                        <p><strong>Willpower:</strong> {stats.willpower}</p>
                        <p><strong>Charisma:</strong> {stats.charisma}</p>
                        <p><strong>Intuition:</strong> {stats.intuition}</p>
                    </div>
                    <div>
                        <h4>Combat Stats</h4>
                        <p><strong>Combat Skill:</strong> {stats.combat_skill}</p>
                        <p><strong>Reaction Time:</strong> {stats.reaction_time}</p>
                        <p><strong>Tactical Awareness:</strong> {stats.tactical_awareness}</p>
                    </div>
                    <div>
                        <h4>Tech Stats</h4>
                        <p><strong>Hacking:</strong> {stats.hacking}</p>
                        <p><strong>Programming:</strong> {stats.programming}</p>
                        <p><strong>Cyber Awareness:</strong> {stats.cyber_awareness}</p>
                    </div>
                </div>
                <p><em>Letzte Aktualisierung: {stats.updated_at}</em></p>
            </div>
            """
            return mark_safe(html)
        except:
            return "Keine Character Stats gefunden"
    character_stats_display.short_description = "Character Stats Übersicht"
