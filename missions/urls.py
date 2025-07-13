from django.urls import path
from .views import (
    ActiveSeasonView, ActiveMissionsView, MissionProgressView, CompletedMissionsView,
    DailyMissionsView, WeeklyMissionsView, SeasonalMissionsView, MissionDetailView,
    MissionCreateView, SeasonCreateView, MissionProgressUpdateView, MissionStatisticsView,
    MissionRewardsView, SeasonListView, MissionListView, UserMissionProgressDetailView
)

app_name = 'missions'

urlpatterns = [
    # Seasons
    path('seasons/', SeasonListView.as_view(), name='season-list'),
    path('seasons/active/', ActiveSeasonView.as_view(), name='active-season'),
    path('seasons/create/', SeasonCreateView.as_view(), name='season-create'),
    
    # Missions - Allgemein
    path('', MissionListView.as_view(), name='mission-list'),
    path('active/', ActiveMissionsView.as_view(), name='active-missions'),
    path('progress/', MissionProgressView.as_view(), name='mission-progress'),
    path('completed/', CompletedMissionsView.as_view(), name='completed-missions'),
    path('create/', MissionCreateView.as_view(), name='mission-create'),
    path('<int:pk>/', MissionDetailView.as_view(), name='mission-detail'),
    
    # Missions nach Typ
    path('daily/', DailyMissionsView.as_view(), name='daily-missions'),
    path('weekly/', WeeklyMissionsView.as_view(), name='weekly-missions'),
    path('seasonal/', SeasonalMissionsView.as_view(), name='seasonal-missions'),
    
    # Fortschritt
    path('progress/update/', MissionProgressUpdateView.as_view(), name='progress-update'),
    path('progress/<int:mission_id>/', UserMissionProgressDetailView.as_view(), name='mission-progress-detail'),
    
    # Statistiken und Belohnungen
    path('statistics/', MissionStatisticsView.as_view(), name='mission-statistics'),
    path('rewards/', MissionRewardsView.as_view(), name='mission-rewards'),
] 