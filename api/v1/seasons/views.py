from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from seasons.models import Season, SeasonXp
from .serializers import SeasonSerializer, SeasonXpSerializer

class ActiveSeasonView(APIView):
    """
    Gibt die aktuell aktive Season zurück.
    """
    def get(self, request):
        season = Season.objects.filter(is_active=True).first()
        if season:
            serializer = SeasonSerializer(season)
            return Response(serializer.data)
        return Response({"detail": "No active season."}, status=status.HTTP_404_NOT_FOUND)

class SeasonRankingView(APIView):
    """
    Gibt das Ranking einer Season + Layer zurück.
    """
    def get(self, request, season_id, layer_type):
        season_xps = SeasonXp.objects.filter(
            season_id=season_id,
            layer_type=layer_type
        ).order_by('-xp')
        serializer = SeasonXpSerializer(season_xps, many=True)
        return Response(serializer.data)
