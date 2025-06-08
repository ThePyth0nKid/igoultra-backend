from django.db import transaction
from seasons.models import Season, SeasonXp
from users.models import User
from rankings.constants import REAL_LAYERS, CYBER_LAYERS
from rankings.models import LayerRankingEntry

def _adjust_layer(current: str, layers: list[str], percentile: float) -> str:
    idx = layers.index(current) if current in layers else 0
    # Aufstieg: Top 10%
    if percentile < 0.10 and idx < len(layers) - 1:
        return layers[idx + 1]
    # Abstieg: untere 20%
    if percentile >= 0.80 and idx > 0:
        return layers[idx - 1]
    return current

@transaction.atomic
def process_season_end(season_id: int):
    season = Season.objects.get(id=season_id)
    sxps   = list(SeasonXp.objects.filter(season=season).select_related("user").order_by("-xp"))
    total  = len(sxps)
    if total == 0:
        return

    # clear old leaderboard entries
    LayerRankingEntry.objects.filter(season=season).delete()

    for pos, sxp in enumerate(sxps):
        p = pos / total
        u = sxp.user

        new_real  = _adjust_layer(u.real_layer,  REAL_LAYERS,  p)
        new_cyber = _adjust_layer(u.cyber_layer, CYBER_LAYERS, p)

        # build snapshot entry
        LayerRankingEntry.objects.create(
            season=season,
            user=u,
            real_layer=new_real,
            cyber_layer=new_cyber,
            xp=sxp.xp
        )

        # update user
        changed = False
        if new_real != u.real_layer:
            u.real_layer = new_real
            changed = True
        if new_cyber != u.cyber_layer:
            u.cyber_layer = new_cyber
            changed = True
        if changed:
            u.save(update_fields=["real_layer", "cyber_layer"])

    # deactivate old and spin up new Season
    season.is_active = False
    season.save(update_fields=["is_active"])
    from datetime import timedelta
    new = Season.objects.create(
        name=f"{season.name} Next",
        start=season.end,
        end=season.end + timedelta(days=90),
        is_active=True
    )
