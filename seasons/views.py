from rest_framework import generics, permissions
from .models import Season, SeasonXp
from ..api.v1.seasons.serializers import SeasonSerializer, SeasonXpSerializer

class ActiveSeasonView(generics.RetrieveAPIView):
    """
    GET /api/v1/seasons/active/ → aktuelle Season
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class   = SeasonSerializer

    def get_object(self):
        return Season.objects.get(is_active=True)

class SeasonXpView(generics.RetrieveAPIView):
    """
    GET /api/v1/seasons/active/xp/ → XP-Summe des Users in der aktuellen Season
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class   = SeasonXpSerializer

    def get_object(self):
        season = Season.objects.get(is_active=True)
        obj, _ = SeasonXp.objects.get_or_create(
            season=season,
            user=self.request.user
        )
        return obj
