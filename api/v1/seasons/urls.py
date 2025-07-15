from django.urls import path, include
from .views import ActiveSeasonView, SeasonRankingView, SeasonListView, SeasonXpListView, SeasonViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', SeasonViewSet, basename='season')

urlpatterns = [
    path('', include(router.urls)),
    path('active/', ActiveSeasonView.as_view(), name='active-season'),
    path('<int:season_id>/ranking/<str:layer_type>/', SeasonRankingView.as_view(), name='season-ranking'),
    path('<int:season_id>/xp/', SeasonXpListView.as_view(), name='season-xp-list'),
]
