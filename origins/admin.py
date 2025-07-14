from django.contrib import admin
from .models import Origin

@admin.register(Origin)
class OriginAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    search_fields = ("name", "type", "description")
