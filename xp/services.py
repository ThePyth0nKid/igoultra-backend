# xp/services.py

from django.db import transaction
from django.utils import timezone

from .models import XpEvent, XpType
from seasons.models import Season, SeasonXp


def xp_for_level(n: int) -> int:
    """
    Kumulativ benötigte XP bis Level n.
    """
    return int(100 * n ** 1.5)


def level_from_xp(total_xp: int) -> int:
    """
    Ermittelt das Level anhand des total_xp-Werts.
    """
    lvl = 1
    while xp_for_level(lvl + 1) <= total_xp:
        lvl += 1
    return lvl


@transaction.atomic
def add_xp_to_user(user, type_key: str, amount_units: float, metadata: dict = None) -> dict:
    """
    Vergibt XP an den User basierend auf XpType:
      1) Holt XpType
      2) Berechnet real_xp = amount_units * xp_amount
      3) Speichert XpEvent
      4) Updated user.xp, user.level und user.rank
      5) Falls eine Season aktiv ist, wird auch SeasonXp upgedatet
    Gibt ein Dict mit total_xp, level, leveled_up und awarded_xp zurück.
    """
    # 1) XpType holen
    xp_type = XpType.objects.get(key=type_key)

    # 2) reale XP berechnen
    real_xp = int(amount_units * xp_type.xp_amount)

    # 3) XpEvent anlegen
    XpEvent.objects.create(
        user=user,
        amount=real_xp,
        source=type_key,
        metadata=metadata or {}
    )

    # 4) User XP & Level updaten
    user.xp = max(0, user.xp + real_xp)
    new_level = level_from_xp(user.xp)
    leveled_up = new_level > user.level
    user.level = new_level
    user.rank = f"Level {new_level}"
    user.save(update_fields=['xp', 'level', 'rank'])

    # 5) SeasonXp aktualisieren, falls eine Season aktiv ist
    today = timezone.now().date()
    try:
        season = Season.objects.get(is_active=True,
                                    start__lte=today,
                                    end__gt=today)
    except Season.DoesNotExist:
        season = None

    if season:
        sxp, _ = SeasonXp.objects.get_or_create(
            season=season,
            user=user
        )
        sxp.xp += real_xp
        sxp.save(update_fields=['xp'])

    return {
        'total_xp': user.xp,
        'level': user.level,
        'leveled_up': leveled_up,
        'awarded_xp': real_xp
    }


def get_xp_stats(user) -> dict:
    """
    Liefert:
      - total_xp: die aktuellen XP
      - level: das berechnete Level
      - xp_to_next: wie viele XP noch zum nächsten Level fehlen
      - next_level_xp: kumulativ benötigte XP für das nächste Level
    """
    total = user.xp
    level = level_from_xp(total)
    next_level = level + 1
    needed = xp_for_level(next_level) - total

    return {
        'total_xp': total,
        'level': level,
        'next_level': next_level,
        'next_level_xp': xp_for_level(next_level),
        'xp_to_next': needed
    }
