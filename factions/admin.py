from django.contrib import admin
from .models import Faction

@admin.register(Faction)
class FactionAdmin(admin.ModelAdmin):
    list_display = ("name", "style", "icon")
    search_fields = ("name", "description", "style")
