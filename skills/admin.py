from django.contrib import admin
from .models import CharacterStats, Skill, UserSkill

@admin.register(CharacterStats)
class CharacterStatsAdmin(admin.ModelAdmin):
    list_display = ['user', 'strength', 'endurance', 'intelligence', 'willpower', 'combat_skill', 'hacking']
    list_filter = ['updated_at']
    search_fields = ['user__username', 'user__ultra_name']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Body Stats', {
            'fields': ('strength', 'endurance', 'agility'),
            'classes': ('collapse',)
        }),
        ('Mind Stats', {
            'fields': ('intelligence', 'focus', 'memory'),
            'classes': ('collapse',)
        }),
        ('Spirit Stats', {
            'fields': ('willpower', 'charisma', 'intuition'),
            'classes': ('collapse',)
        }),
        ('Combat Stats', {
            'fields': ('combat_skill', 'reaction_time', 'tactical_awareness'),
            'classes': ('collapse',)
        }),
        ('Tech Stats', {
            'fields': ('hacking', 'programming', 'cyber_awareness'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'layer', 'tier', 'category', 'required_level', 'is_active']
    list_filter = ['layer', 'tier', 'category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'layer', 'category', 'tier', 'is_active')
        }),
        ('Requirements', {
            'fields': ('required_level', 'required_xp_type', 'required_xp_amount', 'required_stats'),
            'classes': ('collapse',)
        }),
        ('Effects', {
            'fields': ('effects',),
            'classes': ('collapse',)
        }),
    )

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'unlocked_at', 'is_active']
    list_filter = ['skill__layer', 'skill__tier', 'unlocked_at', 'is_active']
    search_fields = ['user__username', 'skill__name']
    readonly_fields = ['unlocked_at']
