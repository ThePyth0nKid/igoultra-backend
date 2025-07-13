from django.db import transaction
from django.utils import timezone

from .models import XpEvent, XpType
from seasons.models import Season, SeasonXp

def xp_for_level(n: int) -> int:
    return int(100 * n ** 1.5)

def level_from_xp(total_xp: int) -> int:
    lvl = 1
    while xp_for_level(lvl + 1) <= total_xp:
        lvl += 1
    return lvl

def get_xp_stats(user) -> dict:
    total = user.xp
    level = level_from_xp(total)
    next_level = level + 1
    next_level_xp = xp_for_level(next_level)
    xp_to_next = next_level_xp - total

    return {
        'total_xp': total,
        'level': level,
        'next_level': next_level,
        'next_level_xp': next_level_xp,
        'xp_to_next': xp_to_next,
    }

@transaction.atomic
def add_xp_to_user(user, type_key: str, amount_units: float, layer_type: str = "Real-Life", metadata: dict = None) -> dict:
    xp_type = XpType.objects.get(key=type_key)
    real_xp = int(amount_units * xp_type.xp_amount)

    XpEvent.objects.create(
        user=user,
        amount=real_xp,
        source=type_key,
        layer_type=layer_type,
        metadata=metadata or {}
    )

    user.xp = max(0, user.xp + real_xp)
    new_level = level_from_xp(user.xp)
    leveled_up = new_level > user.level
    user.level = new_level
    user.save(update_fields=['xp', 'level'])

    # Character Stats aktualisieren (Skills-System)
    try:
        from skills.services import update_character_stats_from_xp
        update_character_stats_from_xp(user, real_xp, xp_type.xp_type)
    except ImportError:
        # Skills-App nicht verfügbar, ignoriere
        pass

    today = timezone.now().date()
    season = Season.objects.filter(is_active=True, start__lte=today, end__gt=today).first()

    if season:
        sxp, _ = SeasonXp.objects.get_or_create(
            season=season,
            user=user,
            layer_type=layer_type,
            defaults={'xp': 0}
        )
        sxp.xp += real_xp
        sxp.save(update_fields=['xp'])

    stats = get_xp_stats(user)
    stats.update({
        'leveled_up': leveled_up,
        'awarded_xp': real_xp,
    })
    return stats
