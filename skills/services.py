from django.db import transaction
from django.db.models import Sum
from .models import CharacterStats, Skill, UserSkill

# XP-Typ zu Stat-Mapping
XP_TO_STATS_MAPPING = {
    'Physical': {
        'strength': 0.3,
        'endurance': 0.4,
        'agility': 0.3,
    },
    'Mental': {
        'intelligence': 0.4,
        'focus': 0.3,
        'memory': 0.3,
    },
    'Cyber': {
        'hacking': 0.4,
        'programming': 0.3,
        'cyber_awareness': 0.3,
    },
    'Ultra': {
        'willpower': 0.3,
        'charisma': 0.2,
        'intuition': 0.3,
        'combat_skill': 0.2,
    }
}

def get_or_create_character_stats(user):
    """
    Erstellt CharacterStats für einen User, falls sie nicht existieren.
    """
    stats, created = CharacterStats.objects.get_or_create(user=user)
    return stats

def calculate_stat_gain(xp_amount, xp_type):
    """
    Berechnet Stat-Gewinn basierend auf XP-Menge und XP-Typ.
    """
    if xp_type not in XP_TO_STATS_MAPPING:
        return {}
    
    stat_gains = {}
    mapping = XP_TO_STATS_MAPPING[xp_type]
    
    # XP in Stat-Punkte umrechnen (1 XP = 0.1 Stat-Punkte)
    base_stat_gain = xp_amount * 0.1
    
    for stat_name, multiplier in mapping.items():
        stat_gains[stat_name] = int(base_stat_gain * multiplier)
    
    return stat_gains

@transaction.atomic
def update_character_stats_from_xp(user, xp_amount, xp_type):
    """
    Aktualisiert CharacterStats basierend auf neuem XP.
    """
    stats = get_or_create_character_stats(user)
    stat_gains = calculate_stat_gain(xp_amount, xp_type)
    
    # Stats erhöhen (mit Max-Wert von 100)
    for stat_name, gain in stat_gains.items():
        if hasattr(stats, stat_name):
            current_value = getattr(stats, stat_name)
            new_value = min(100, current_value + gain)
            setattr(stats, stat_name, new_value)
    
    stats.save()
    return stats

def get_user_stats(user):
    """
    Gibt alle Stats eines Users zurück.
    """
    try:
        stats = user.character_stats
        return stats.get_all_stats()
    except CharacterStats.DoesNotExist:
        # Erstelle Stats falls sie nicht existieren
        stats = get_or_create_character_stats(user)
        return stats.get_all_stats()

def get_available_skills(user):
    """
    Gibt alle verfügbaren Skills für einen User zurück.
    """
    skills = Skill.objects.filter(is_active=True)
    available_skills = []
    
    for skill in skills:
        can_unlock, message = skill.check_requirements(user)
        available_skills.append({
            'skill': skill,
            'can_unlock': can_unlock,
            'message': message,
            'is_unlocked': UserSkill.objects.filter(user=user, skill=skill, is_active=True).exists()
        })
    
    return available_skills

def get_user_skills(user):
    """
    Gibt alle freigeschalteten Skills eines Users zurück.
    """
    return UserSkill.objects.filter(user=user, is_active=True).select_related('skill')

@transaction.atomic
def unlock_skill(user, skill_id):
    """
    Versucht einen Skill für einen User freizuschalten.
    """
    try:
        skill = Skill.objects.get(id=skill_id, is_active=True)
    except Skill.DoesNotExist:
        return False, "Skill nicht gefunden"
    
    # Prüfe ob bereits freigeschaltet
    if UserSkill.objects.filter(user=user, skill=skill, is_active=True).exists():
        return False, "Skill bereits freigeschaltet"
    
    # Prüfe Voraussetzungen
    can_unlock, message = skill.check_requirements(user)
    if not can_unlock:
        return False, message
    
    # Skill freischalten
    UserSkill.objects.create(user=user, skill=skill)
    return True, f"Skill '{skill.name}' erfolgreich freigeschaltet!"

def get_skill_progress(user, skill):
    """
    Gibt den Fortschritt für einen Skill zurück.
    """
    progress = {
        'skill': skill,
        'requirements_met': {},
        'overall_progress': 0
    }
    
    # Level-Progress
    level_progress = min(100, (user.level / skill.required_level) * 100)
    progress['requirements_met']['level'] = {
        'current': user.level,
        'required': skill.required_level,
        'progress': level_progress
    }
    
    # XP-Typ-Progress
    if skill.required_xp_type and skill.required_xp_amount > 0:
        total_xp_in_type = user.xp_events.filter(
            source__startswith=skill.required_xp_type.lower()
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        xp_progress = min(100, (total_xp_in_type / skill.required_xp_amount) * 100)
        progress['requirements_met']['xp'] = {
            'current': total_xp_in_type,
            'required': skill.required_xp_amount,
            'progress': xp_progress
        }
    
    # Stat-Progress
    if skill.required_stats:
        try:
            stats = user.character_stats
            stat_progress = {}
            for stat_name, required_value in skill.required_stats.items():
                current_value = stats.get_stat(stat_name)
                stat_progress_value = min(100, (current_value / required_value) * 100)
                stat_progress[stat_name] = {
                    'current': current_value,
                    'required': required_value,
                    'progress': stat_progress_value
                }
            progress['requirements_met']['stats'] = stat_progress
        except CharacterStats.DoesNotExist:
            progress['requirements_met']['stats'] = {}
    
    # Gesamtfortschritt berechnen
    total_progress = 0
    count = 0
    for req_type, req_data in progress['requirements_met'].items():
        if req_type == 'stats':
            for stat_name, stat_data in req_data.items():
                total_progress += stat_data['progress']
                count += 1
        else:
            total_progress += req_data['progress']
            count += 1
    
    if count > 0:
        progress['overall_progress'] = total_progress / count
    
    return progress 