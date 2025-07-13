from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Season, Mission, MissionProgress
from .serializers import (
    SeasonSerializer, MissionSerializer, MissionProgressSerializer,
    ActiveMissionSerializer, CompletedMissionSerializer,
    MissionCreateSerializer, SeasonCreateSerializer,
    MissionProgressUpdateSerializer, MissionRewardSerializer
)
from .services import (
    get_active_season, get_active_missions_for_user, get_user_mission_progress,
    get_completed_missions_for_user, update_mission_progress_for_activity,
    get_mission_statistics_for_user, get_daily_missions, get_weekly_missions,
    get_seasonal_missions
)

class ActiveSeasonView(generics.RetrieveAPIView):
    """
    GET /api/v1/missions/seasons/active/ → Aktuelle aktive Season
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SeasonSerializer
    
    def get_object(self):
        season = get_active_season()
        if not season:
            return None
        return season
    
    def retrieve(self, request, *args, **kwargs):
        season = self.get_object()
        if not season:
            return Response({
                'message': 'Keine aktive Season gefunden'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(season)
        return Response(serializer.data)

class ActiveMissionsView(generics.ListAPIView):
    """
    GET /api/v1/missions/active/ → Alle aktiven Missionen für den User
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ActiveMissionSerializer
    
    def get_queryset(self):
        mission_type = self.request.query_params.get('mission_type')
        return get_active_missions_for_user(self.request.user, mission_type)

class MissionProgressView(generics.ListAPIView):
    """
    GET /api/v1/missions/progress/ → Fortschritt für alle Missionen des Users
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MissionProgressSerializer
    
    def get_queryset(self):
        mission_type = self.request.query_params.get('mission_type')
        return get_user_mission_progress(self.request.user, mission_type)

class CompletedMissionsView(generics.ListAPIView):
    """
    GET /api/v1/missions/completed/ → Abgeschlossene Missionen des Users
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CompletedMissionSerializer
    
    def get_queryset(self):
        mission_type = self.request.query_params.get('mission_type')
        return get_completed_missions_for_user(self.request.user, mission_type)

class DailyMissionsView(generics.ListAPIView):
    """
    GET /api/v1/missions/daily/ → Alle aktiven Daily-Missionen
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ActiveMissionSerializer
    
    def get_queryset(self):
        return get_daily_missions()

class WeeklyMissionsView(generics.ListAPIView):
    """
    GET /api/v1/missions/weekly/ → Alle aktiven Weekly-Missionen
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ActiveMissionSerializer
    
    def get_queryset(self):
        return get_weekly_missions()

class SeasonalMissionsView(generics.ListAPIView):
    """
    GET /api/v1/missions/seasonal/ → Alle aktiven Seasonal-Missionen
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ActiveMissionSerializer
    
    def get_queryset(self):
        return get_seasonal_missions()

class MissionDetailView(generics.RetrieveAPIView):
    """
    GET /api/v1/missions/{id}/ → Detail einer Mission
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MissionSerializer
    queryset = Mission.objects.filter(is_active=True)

class MissionCreateView(generics.CreateAPIView):
    """
    POST /api/v1/missions/create/ → Neue Mission erstellen (Admin)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MissionCreateSerializer
    queryset = Mission.objects.all()

class SeasonCreateView(generics.CreateAPIView):
    """
    POST /api/v1/missions/seasons/create/ → Neue Season erstellen (Admin)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SeasonCreateSerializer
    queryset = Season.objects.all()

class MissionProgressUpdateView(generics.GenericAPIView):
    """
    POST /api/v1/missions/progress/update/ → Fortschritt manuell aktualisieren
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MissionProgressUpdateSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        unit = request.data.get('unit')
        if not unit:
            return Response({
                'error': 'Unit ist erforderlich'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        result = serializer.update_progress(request.user, unit)
        return Response(result, status=status.HTTP_200_OK)

class MissionStatisticsView(generics.GenericAPIView):
    """
    GET /api/v1/missions/statistics/ → Mission-Statistiken für den User
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        stats = get_mission_statistics_for_user(request.user)
        return Response(stats, status=status.HTTP_200_OK)

class MissionRewardsView(generics.GenericAPIView):
    """
    GET /api/v1/missions/rewards/ → Belohnungen für abgeschlossene Missionen
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MissionRewardSerializer
    
    def get(self, request, *args, **kwargs):
        completed_missions = get_completed_missions_for_user(request.user)
        
        total_rewards = {
            'xp': sum(progress.mission.xp_reward for progress in completed_missions),
            'gold': sum(progress.mission.gold_reward for progress in completed_missions),
            'ultra_points': sum(progress.mission.ultra_point_reward for progress in completed_missions),
        }
        
        serializer = self.get_serializer(total_rewards)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SeasonListView(generics.ListAPIView):
    """
    GET /api/v1/missions/seasons/ → Liste aller Seasons
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SeasonSerializer
    queryset = Season.objects.all().order_by('-start_date')

class MissionListView(generics.ListAPIView):
    """
    GET /api/v1/missions/ → Liste aller Missionen (Admin)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MissionSerializer
    queryset = Mission.objects.all().order_by('mission_type', 'created_at')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter nach Mission-Typ
        mission_type = self.request.query_params.get('mission_type')
        if mission_type:
            queryset = queryset.filter(mission_type=mission_type)
        
        # Filter nach Unit
        unit = self.request.query_params.get('unit')
        if unit:
            queryset = queryset.filter(unit=unit)
        
        # Filter nach Status
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset

class UserMissionProgressDetailView(generics.RetrieveAPIView):
    """
    GET /api/v1/missions/progress/{mission_id}/ → Detail-Fortschritt für eine Mission
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MissionProgressSerializer
    
    def get_object(self):
        mission_id = self.kwargs.get('mission_id')
        mission = get_object_or_404(Mission, id=mission_id)
        
        progress, created = MissionProgress.objects.get_or_create(
            user=self.request.user,
            mission=mission,
            defaults={'current_value': 0}
        )
        
        return progress
