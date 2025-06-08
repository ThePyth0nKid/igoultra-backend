# api/v1/rankings/views.py

from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from rankings.constants import REAL_LAYERS, CYBER_LAYERS
from rankings.models import LayerRankingEntry
from rankings.serializers import LayerRankingEntrySerializer


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="season",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=True,
                description="ID der Season, für die das Leaderboard angezeigt werden soll",
            ),
            OpenApiParameter(
                name="real_layer",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter für Realitäts-Layer (BaseLayer, EmotionLayer, …)",
                enum=REAL_LAYERS,
            ),
            OpenApiParameter(
                name="cyber_layer",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter für Cyber-Layer (SurfaceWebLayer, DeepNetLayer, …)",
                enum=CYBER_LAYERS,
            ),
            OpenApiParameter(
                name="top",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Anzahl der Top-Einträge (Standard: 10)",
            ),
        ]
    )
)
class LeaderboardView(generics.ListAPIView):
    """
    GET /api/v1/rankings/leaderboard/
    Query-Parameter:
      - season (int, required)
      - real_layer (string, optional)   z.B. BaseLayer
      - cyber_layer (string, optional)  z.B. SurfaceWebLayer
      - top (int, optional, default=10)
    Liefert die Top-N Einträge (user, xp, real_layer, cyber_layer),
    sortiert nach XP absteigend.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class   = LayerRankingEntrySerializer

    def get_queryset(self):
        season_id   = self.request.query_params.get("season")
        real_layer  = self.request.query_params.get("real_layer")
        cyber_layer = self.request.query_params.get("cyber_layer")
        top         = int(self.request.query_params.get("top", 10))

        # Nur weiter, wenn season und mindestens einer der Layer-Filter gesetzt ist
        if not season_id or (not real_layer and not cyber_layer):
            return LayerRankingEntry.objects.none()

        filters = {"season_id": season_id}
        if real_layer:
            filters["real_layer"] = real_layer
        else:
            filters["cyber_layer"] = cyber_layer

        return (
            LayerRankingEntry.objects
            .filter(**filters)
            .order_by("-xp")[:top]
        )
