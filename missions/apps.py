from django.apps import AppConfig


class MissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'missions'
    verbose_name = 'Missions System'
    
    def ready(self):
        """Wird beim Start der App ausgeführt"""
        import missions.signals
