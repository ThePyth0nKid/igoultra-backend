from django.urls import path
from .views import ActiveSeasonView, SeasonRankingView, SeasonListView, SeasonXpListView

urlpatterns = [
    path('', SeasonListView.as_view(), name='season-list'),
    path('active/', ActiveSeasonView.as_view(), name='active-season'),
    path('<int:season_id>/ranking/<str:layer_type>/', SeasonRankingView.as_view(), name='season-ranking'),
    path('<int:season_id>/xp/', SeasonXpListView.as_view(), name='season-xp-list'),
]
