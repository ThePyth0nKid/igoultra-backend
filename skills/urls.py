from django.urls import path
from .views import (
    StatsOverviewView, AvailableSkillsView, UserSkillsView,
    SkillProgressView, UnlockSkillView, SkillListView
)

app_name = 'skills'

urlpatterns = [
    # Stats
    path('stats/', StatsOverviewView.as_view(), name='stats-overview'),
    
    # Skills
    path('', SkillListView.as_view(), name='skill-list'),
    path('available/', AvailableSkillsView.as_view(), name='available-skills'),
    path('unlocked/', UserSkillsView.as_view(), name='user-skills'),
    path('unlock/', UnlockSkillView.as_view(), name='unlock-skill'),
    path('<int:skill_id>/progress/', SkillProgressView.as_view(), name='skill-progress'),
] 