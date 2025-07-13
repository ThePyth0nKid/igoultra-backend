from django.utils import timezone
from django.db.models import Q
from .models import Season, Mission, MissionProgress

def get_active_season():
    """Gibt die aktuell aktive Season zurück"""
    return Season.get_active_season()

def get_active_missions_for_user(user, mission_type=None):
    """
    Gibt alle aktiven Missionen für einen User zurück.
    Optional gefiltert nach Mission-Typ.
    """
    # Basis-Query für aktive Missionen
    missions = Mission.objects.filter(is_active=True)
    
    # Filter nach Mission-Typ
    if mission_type:
        missions = missions.filter(mission_type=mission_type)
    
    # Prüfe Zeitrahmen
    now = timezone.now()
    missions = missions.filter(
        Q(start_time__isnull=True) | Q(start_time__lte=now)
    ).filter(
        Q(end_time__isnull=True) | Q(end_time__gte=now)
    )
    
    # Prüfe Season für saisonale Missionen
    if not mission_type or mission_type == 'seasonal':
        active_season = get_active_season()
        if active_season:
            seasonal_missions = Mission.objects.filter(
                mission_type='seasonal',
                season=active_season,
                is_active=True
            )
            # Kombiniere die Querysets ohne union()
            missions = missions | seasonal_missions
    
    return missions

def get_user_mission_progress(user, mission_type=None):
    """
    Gibt den Fortschritt eines Users für alle Missionen zurück.
    Optional gefiltert nach Mission-Typ.
    """
    progress = MissionProgress.objects.filter(user=user)
    
    if mission_type:
        progress = progress.filter(mission__mission_type=mission_type)
    
    return progress.select_related('mission')

def get_completed_missions_for_user(user, mission_type=None):
    """
    Gibt alle abgeschlossenen Missionen eines Users zurück.
    Optional gefiltert nach Mission-Typ.
    """
    progress = MissionProgress.objects.filter(
        user=user,
        is_completed=True
    )
    
    if mission_type:
        progress = progress.filter(mission__mission_type=mission_type)
    
    return progress.select_related('mission').order_by('-completed_at')

def create_mission_progress_for_user(user, mission):
    """
    Erstellt einen neuen Fortschritt für einen User und eine Mission.
    """
    return MissionProgress.create_progress_for_user(user, mission)

def update_mission_progress_for_activity(user, unit, value=1):
    """
    Aktualisiert den Fortschritt für alle passenden Missionen basierend auf einer Aktivität.
    """
    MissionProgress.update_progress_for_activity(user, unit, value)

def get_daily_missions():
    """Gibt alle aktiven Daily-Missionen zurück"""
    return Mission.get_daily_missions()

def get_weekly_missions():
    """Gibt alle aktiven Weekly-Missionen zurück"""
    return Mission.get_weekly_missions()

def get_seasonal_missions():
    """Gibt alle aktiven Seasonal-Missionen zurück"""
    return Mission.get_seasonal_missions()

def get_mission_statistics_for_user(user):
    """
    Gibt Statistiken über Missionen für einen User zurück.
    """
    total_progress = MissionProgress.objects.filter(user=user)
    completed_missions = total_progress.filter(is_completed=True)
    
    # Statistiken nach Mission-Typ
    daily_stats = {
        'total': total_progress.filter(mission__mission_type='daily').count(),
        'completed': completed_missions.filter(mission__mission_type='daily').count(),
    }
    
    weekly_stats = {
        'total': total_progress.filter(mission__mission_type='weekly').count(),
        'completed': completed_missions.filter(mission__mission_type='weekly').count(),
    }
    
    seasonal_stats = {
        'total': total_progress.filter(mission__mission_type='seasonal').count(),
        'completed': completed_missions.filter(mission__mission_type='seasonal').count(),
    }
    
    # Belohnungen
    total_rewards = {
        'xp': sum(progress.mission.xp_reward for progress in completed_missions),
        'gold': sum(progress.mission.gold_reward for progress in completed_missions),
        'ultra_points': sum(progress.mission.ultra_point_reward for progress in completed_missions),
    }
    
    return {
        'daily': daily_stats,
        'weekly': weekly_stats,
        'seasonal': seasonal_stats,
        'total_rewards': total_rewards,
        'total_completed': completed_missions.count(),
        'total_missions': total_progress.count(),
    }

def check_and_create_daily_missions():
    """
    Prüft und erstellt neue Daily-Missionen für alle User.
    Sollte täglich ausgeführt werden.
    """
    daily_missions = get_daily_missions()
    
    # Hier könnte Logik für das automatische Erstellen von Daily-Missionen stehen
    # z.B. basierend auf User-Level, vorherigen Aktivitäten, etc.
    
    return daily_missions

def check_and_create_weekly_missions():
    """
    Prüft und erstellt neue Weekly-Missionen für alle User.
    Sollte wöchentlich ausgeführt werden.
    """
    weekly_missions = get_weekly_missions()
    
    # Hier könnte Logik für das automatische Erstellen von Weekly-Missionen stehen
    
    return weekly_missions

def reset_expired_missions():
    """
    Setzt abgelaufene Missionen zurück.
    Sollte regelmäßig ausgeführt werden.
    """
    now = timezone.now()
    
    # Finde abgelaufene Missionen
    expired_missions = Mission.objects.filter(
        is_active=True,
        end_time__lt=now
    )
    
    # Deaktiviere abgelaufene Missionen
    expired_missions.update(is_active=False)
    
    return expired_missions.count()

def award_mission_rewards(user, mission_progress):
    """
    Vergibt Belohnungen für eine abgeschlossene Mission.
    """
    mission = mission_progress.mission
    
    # XP-Belohnung
    if mission.xp_reward > 0:
        # Hier würde die XP-Vergabe-Logik stehen
        # user.add_xp(mission.xp_reward)
        pass
    
    # Gold-Belohnung
    if mission.gold_reward > 0:
        # Hier würde die Gold-Vergabe-Logik stehen
        # user.add_gold(mission.gold_reward)
        pass
    
    # Ultra-Point-Belohnung
    if mission.ultra_point_reward > 0:
        # Hier würde die Ultra-Point-Vergabe-Logik stehen
        # user.add_ultra_points(mission.ultra_point_reward)
        pass
    
    return {
        'xp': mission.xp_reward,
        'gold': mission.gold_reward,
        'ultra_points': mission.ultra_point_reward,
    }

def get_mission_suggestions_for_user(user):
    """
    Gibt Mission-Vorschläge für einen User basierend auf seinen Aktivitäten zurück.
    """
    # Hier könnte Logik für personalisierte Mission-Vorschläge stehen
    # z.B. basierend auf User-Level, vorherigen Aktivitäten, etc.
    
    suggestions = []
    
    # Beispiel: Vorschläge basierend auf User-Level
    if user.level < 10:
        suggestions.append({
            'type': 'daily',
            'title': 'Erste Schritte',
            'description': 'Sammle 100 XP',
            'unit': 'xp_gained',
            'target_value': 100,
        })
    
    return suggestions 