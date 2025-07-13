from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Mission, MissionProgress
from .services import update_mission_progress_for_activity

User = get_user_model()

@receiver(post_save, sender=Mission)
def create_mission_progress_for_existing_users(sender, instance, created, **kwargs):
    """
    Erstellt Mission-Progress für alle existierenden User, wenn eine neue Mission erstellt wird.
    """
    if created and instance.is_active:
        for user in User.objects.all():
            MissionProgress.create_progress_for_user(user, instance)

@receiver(post_save, sender=MissionProgress)
def award_rewards_on_completion(sender, instance, created, **kwargs):
    """
    Vergibt Belohnungen, wenn eine Mission abgeschlossen wird.
    """
    if instance.is_completed and instance.completed_at:
        # Hier würde die Belohnungs-Logik stehen
        # award_mission_rewards(instance.user, instance)
        pass

# Signal für XP-Events (wenn XP-System verfügbar ist)
@receiver(post_save, sender='xp.XPEvent')
def update_missions_on_xp_gain(sender, instance, created, **kwargs):
    """
    Aktualisiert Mission-Fortschritt basierend auf XP-Gewinn.
    """
    if created:
        update_mission_progress_for_activity(
            user=instance.user,
            unit='xp_gained',
            value=instance.amount
        )

# Signal für Skill-Events (wenn Skill-System verfügbar ist)
@receiver(post_save, sender='skills.UserSkill')
def update_missions_on_skill_unlock(sender, instance, created, **kwargs):
    """
    Aktualisiert Mission-Fortschritt basierend auf Skill-Freischaltung.
    """
    if created:
        update_mission_progress_for_activity(
            user=instance.user,
            unit='skills_unlocked',
            value=1
        )

# Signal für Layer-Events (wenn Layer-System verfügbar ist)
@receiver(post_save, sender='layers.UserLayerProgress')
def update_missions_on_layer_completion(sender, instance, created, **kwargs):
    """
    Aktualisiert Mission-Fortschritt basierend auf Layer-Abschluss.
    """
    if instance.is_completed:
        update_mission_progress_for_activity(
            user=instance.user,
            unit='layers_completed',
            value=1
        ) 