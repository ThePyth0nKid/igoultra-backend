# api/v1/rankings/urls.py
from django.urls import path
from .views import LeaderboardView

urlpatterns = [
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
]
