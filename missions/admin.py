from django.contrib import admin
from .models import Season, Mission, MissionProgress

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'is_active', 'created_at']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description')
        }),
        ('Time Settings', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Validiert, dass nur eine Season gleichzeitig aktiv sein kann"""
        if obj.is_active:
            # Deaktiviere andere aktive Seasons
            Season.objects.filter(is_active=True).exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'mission_type', 'unit', 'target_value', 'is_active', 'created_at']
    list_filter = ['mission_type', 'unit', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'mission_type', 'unit', 'target_value')
        }),
        ('Rewards', {
            'fields': ('xp_reward', 'gold_reward', 'ultra_point_reward')
        }),
        ('Time Settings', {
            'fields': ('start_time', 'end_time', 'season')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimiert die Query mit select_related"""
        return super().get_queryset(request).select_related('season')

@admin.register(MissionProgress)
class MissionProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'mission', 'current_value', 'target_value', 'progress_percentage', 'is_completed', 'updated_at']
    list_filter = ['is_completed', 'mission__mission_type', 'created_at', 'updated_at']
    search_fields = ['user__username', 'mission__title']
    readonly_fields = ['created_at', 'updated_at', 'progress_percentage']
    
    fieldsets = (
        ('User & Mission', {
            'fields': ('user', 'mission')
        }),
        ('Progress', {
            'fields': ('current_value', 'target_value', 'progress_percentage', 'is_completed', 'completed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def progress_percentage(self, obj):
        """Zeigt den Fortschritt in Prozent an"""
        return f"{obj.get_progress_percentage():.1f}%"
    progress_percentage.short_description = "Progress %"
    
    def target_value(self, obj):
        """Zeigt den Zielwert an"""
        return obj.mission.target_value
    target_value.short_description = "Target"
    
    def get_queryset(self, request):
        """Optimiert die Query mit select_related"""
        return super().get_queryset(request).select_related('user', 'mission')
