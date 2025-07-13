from django.urls import path
from .views import (
    StatsOverviewView, AvailableSkillsView, UserSkillsView,
    SkillProgressView, UnlockSkillView, SkillListView,
    ActiveSkillsView, PassiveSkillsView, SkillDetailView, SkillCreateView,
    UserActiveSkillsView, UserPassiveSkillsView
)

app_name = 'skills'

urlpatterns = [
    # Stats
    path('stats/', StatsOverviewView.as_view(), name='stats-overview'),
    
    # Skills - Allgemein
    path('', SkillListView.as_view(), name='skill-list'),
    path('available/', AvailableSkillsView.as_view(), name='available-skills'),
    path('unlocked/', UserSkillsView.as_view(), name='user-skills'),
    path('unlock/', UnlockSkillView.as_view(), name='unlock-skill'),
    path('<int:skill_id>/progress/', SkillProgressView.as_view(), name='skill-progress'),
    path('<int:pk>/', SkillDetailView.as_view(), name='skill-detail'),
    path('create/', SkillCreateView.as_view(), name='skill-create'),
    
    # Aktive Skills
    path('active/', ActiveSkillsView.as_view(), name='active-skills'),
    path('unlocked/active/', UserActiveSkillsView.as_view(), name='user-active-skills'),
    
    # Passive Skills
    path('passive/', PassiveSkillsView.as_view(), name='passive-skills'),
    path('unlocked/passive/', UserPassiveSkillsView.as_view(), name='user-passive-skills'),
] 