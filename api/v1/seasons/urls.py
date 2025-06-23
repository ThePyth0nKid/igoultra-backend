from django.urls import path
from .views import ActiveSeasonView, SeasonRankingView

urlpatterns = [
    path('active/', ActiveSeasonView.as_view(), name='active-season'),
    path('<int:season_id>/ranking/<str:layer_type>/', SeasonRankingView.as_view(), name='season-ranking'),
]
