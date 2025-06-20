from django.contrib import admin
from .models import LayerRankingEntry

@admin.register(LayerRankingEntry)
class LayerRankingEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'season', 'layer_type', 'xp')
    list_filter = ('season', 'layer_type')
    search_fields = ('user__username', 'season__name')
