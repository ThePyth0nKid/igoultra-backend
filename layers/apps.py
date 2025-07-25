from django.apps import AppConfig


class LayersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'layers'

    def ready(self):
        import layers.signals
