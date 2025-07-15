from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from seasons.models import Season, SeasonXp
from .serializers import SeasonSerializer, SeasonXpSerializer
from rest_framework import generics
from rest_framework import viewsets, permissions

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

class SeasonListView(generics.ListAPIView):
    queryset = Season.objects.all().order_by('-start')
    serializer_class = SeasonSerializer

class SeasonXpListView(generics.ListAPIView):
    serializer_class = SeasonXpSerializer

    def get_queryset(self):
        season_id = self.kwargs['season_id']
        layer_type = self.request.query_params.get('layer_type')
        qs = SeasonXp.objects.filter(season_id=season_id)
        if layer_type:
            qs = qs.filter(layer_type=layer_type)
        return qs.order_by('-xp')

class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff

class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all().order_by('-start')
    serializer_class = SeasonSerializer
    permission_classes = [IsStaffOrReadOnly]
