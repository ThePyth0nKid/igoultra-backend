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


def get_xp_stats(user) -> dict:
    """
    Liefert:
      - total_xp: die aktuellen XP
      - level: das berechnete Level
      - next_level: das nächste Level
      - next_level_xp: kumulativ benötigte XP für das nächste Level
      - xp_to_next: wie viele XP noch zum nächsten Level fehlen
    """
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
def add_xp_to_user(user, type_key: str, amount_units: float, metadata: dict = None) -> dict:
    """
    Vergibt XP an den User basierend auf XpType:
      1) Holt XpType
      2) Berechnet real_xp = amount_units * xp_amount
      3) Speichert XpEvent
      4) Updated user.xp und user.level
      5) Falls eine Season aktiv ist, wird auch SeasonXp upgedatet
    Gibt ein Dict mit den aktuellen Stats und awarded_xp zurück:
      - total_xp
      - level
      - next_level
      - next_level_xp
      - xp_to_next
      - leveled_up (bool)
      - awarded_xp
    """
    # 1) XP-Typ holen
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

    # 4) User XP & Level updaten (ohne rank!)
    user.xp = max(0, user.xp + real_xp)
    new_level = level_from_xp(user.xp)
    leveled_up = new_level > user.level
    user.level = new_level
    # user.rank nicht hier setzen – bleibt für Community-Ränge frei
    user.save(update_fields=['xp', 'level'])

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

    # 6) Aktuelle XP-Stats holen und erweitern
    stats = get_xp_stats(user)
    stats.update({
        'leveled_up': leveled_up,
        'awarded_xp': real_xp,
    })
    return stats
