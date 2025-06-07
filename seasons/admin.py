from django.contrib import admin
from .models import Season, SeasonXp

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("name", "start", "end", "is_active")
    list_filter  = ("is_active",)

@admin.register(SeasonXp)
class SeasonXpAdmin(admin.ModelAdmin):
    list_display = ("user", "season", "xp")
    list_filter  = ("season",)
    search_fields = ("user__username",)
