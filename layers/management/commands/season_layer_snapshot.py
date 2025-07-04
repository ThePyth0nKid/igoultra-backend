from django.core.management.base import BaseCommand
from rankings.models import LayerRankingEntry
from layers.models import Layer, UserLayerProgress
from seasons.models import Season

class Command(BaseCommand):
    help = "Führt den Layer-Snapshot am Saisonende durch (Auf-/Abstieg auf Basis LayerRankingEntry)."

    def handle(self, *args, **options):
        # Letzte (abgeschlossene) Season finden
        season = Season.objects.filter(is_active=False).order_by('-end').first()
        if not season:
            self.stderr.write("Keine abgeschlossene Season gefunden.")
            return

        for layer_type in ['real', 'cyber']:
            layers = list(Layer.objects.filter(type=layer_type).order_by('order'))
            for i, layer in enumerate(layers):
                entries = LayerRankingEntry.objects.filter(season=season, layer_type=layer.code).order_by('-xp')
                total = entries.count()
                if total == 0:
                    continue
                top_cut = int(total * 0.1)
                bottom_cut = int(total * 0.1)
                # Aufsteiger
                if i < len(layers) - 1:
                    next_layer = layers[i+1]
                    for entry in entries[:top_cut]:
                        progress = UserLayerProgress.objects.get(user=entry.user)
                        if layer_type == 'real':
                            progress.real_layer = next_layer
                        else:
                            progress.cyber_layer = next_layer
                        progress.save()
                # Absteiger
                if i > 0:
                    prev_layer = layers[i-1]
                    for entry in entries[-bottom_cut:]:
                        progress = UserLayerProgress.objects.get(user=entry.user)
                        if layer_type == 'real':
                            progress.real_layer = prev_layer
                        else:
                            progress.cyber_layer = prev_layer
                        progress.save()
        self.stdout.write(self.style.SUCCESS("Layer-Snapshot abgeschlossen.")) 