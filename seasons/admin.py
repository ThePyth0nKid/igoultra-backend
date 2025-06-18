from django.contrib import admin
from .models import Season, SeasonXp

# Global Admin Branding
admin.site.site_header = "IGOULTRA Admin"
admin.site.site_title = "IGOULTRA Admin Portal"
admin.site.index_title = "Willkommen im IGOULTRA Admin-Bereich"

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("name", "start", "end", "is_active")
    list_filter  = ("is_active",)

@admin.register(SeasonXp)
class SeasonXpAdmin(admin.ModelAdmin):
    list_display = ("user", "season", "xp")
    list_filter  = ("season",)
    search_fields = ("user__username",)
