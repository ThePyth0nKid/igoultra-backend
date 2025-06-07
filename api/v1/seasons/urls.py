from django.urls import path
from seasons.views import ActiveSeasonView, SeasonXpView

urlpatterns = [
    # GET  /api/v1/seasons/active/    → Details der aktiven Season
    path("active/", ActiveSeasonView.as_view(), name="active-season"),
    # GET  /api/v1/seasons/active/xp/ → Season-XP des eingeloggten Users
    path("active/xp/", SeasonXpView.as_view(), name="active-season-xp"),
]
