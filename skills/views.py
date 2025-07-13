from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Skill, UserSkill
from .serializers import (
    SkillSerializer, UserSkillSerializer, SkillProgressSerializer,
    AvailableSkillSerializer, UnlockSkillSerializer, StatsOverviewSerializer,
    ActiveSkillSerializer, PassiveSkillSerializer, SkillCreateSerializer
)
from .services import (
    get_user_stats, get_available_skills, get_user_skills,
    unlock_skill, get_skill_progress
)

class StatsOverviewView(generics.GenericAPIView):
    """
    GET /api/v1/skills/stats/ → Übersicht aller Character-Stats
    """
    permission_classes = [IsAuthenticated]
    serializer_class = StatsOverviewSerializer

    def get(self, request, *args, **kwargs):
        stats = get_user_stats(request.user)
        serializer = self.get_serializer(stats)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AvailableSkillsView(generics.GenericAPIView):
    """
    GET /api/v1/skills/available/ → Alle verfügbaren Skills mit Status
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AvailableSkillSerializer

    def get(self, request, *args, **kwargs):
        available_skills = get_available_skills(request.user)
        
        # Filter nach Layer falls angegeben
        layer = request.query_params.get('layer')
        if layer:
            available_skills = [skill for skill in available_skills if skill['skill'].layer == layer]
        
        # Filter nach Kategorie falls angegeben
        category = request.query_params.get('category')
        if category:
            available_skills = [skill for skill in available_skills if skill['skill'].category == category]
        
        # Filter nach Skill-Typ falls angegeben
        skill_type = request.query_params.get('skill_type')
        if skill_type:
            available_skills = [skill for skill in available_skills if skill['skill'].skill_type == skill_type]
        
        serializer = self.get_serializer(available_skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserSkillsView(generics.ListAPIView):
    """
    GET /api/v1/skills/unlocked/ → Alle freigeschalteten Skills des Users
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSkillSerializer

    def get_queryset(self):
        return get_user_skills(self.request.user)

class SkillProgressView(generics.GenericAPIView):
    """
    GET /api/v1/skills/{skill_id}/progress/ → Fortschritt für einen spezifischen Skill
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SkillProgressSerializer

    def get(self, request, skill_id, *args, **kwargs):
        skill = get_object_or_404(Skill, id=skill_id, is_active=True)
        progress = get_skill_progress(request.user, skill)
        
        # Prüfe ob Skill freigeschaltet werden kann
        can_unlock, message = skill.check_requirements(request.user)
        is_unlocked = UserSkill.objects.filter(user=request.user, skill=skill, is_active=True).exists()
        
        progress.update({
            'can_unlock': can_unlock,
            'message': message,
            'is_unlocked': is_unlocked
        })
        
        serializer = self.get_serializer(progress)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UnlockSkillView(generics.GenericAPIView):
    """
    POST /api/v1/skills/unlock/ → Skill freischalten
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UnlockSkillSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        skill_id = serializer.validated_data['skill_id']
        success, message = unlock_skill(request.user, skill_id)
        
        if success:
            return Response({
                'success': True,
                'message': message
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': message
            }, status=status.HTTP_400_BAD_REQUEST)

class SkillListView(generics.ListAPIView):
    """
    GET /api/v1/skills/ → Liste aller Skills (Admin/Übersicht)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SkillSerializer
    queryset = Skill.objects.filter(is_active=True)

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter nach Layer
        layer = self.request.query_params.get('layer')
        if layer:
            queryset = queryset.filter(layer=layer)
        
        # Filter nach Kategorie
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter nach Tier
        tier = self.request.query_params.get('tier')
        if tier:
            queryset = queryset.filter(tier=tier)
        
        # Filter nach Skill-Typ
        skill_type = self.request.query_params.get('skill_type')
        if skill_type:
            queryset = queryset.filter(skill_type=skill_type)
        
        return queryset

class ActiveSkillsView(generics.ListAPIView):
    """
    GET /api/v1/skills/active/ → Liste aller aktiven Skills
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ActiveSkillSerializer
    queryset = Skill.objects.filter(is_active=True, skill_type='active')

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter nach Layer
        layer = self.request.query_params.get('layer')
        if layer:
            queryset = queryset.filter(layer=layer)
        
        # Filter nach Kategorie
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter nach Effekt-Typ
        effect_type = self.request.query_params.get('effect_type')
        if effect_type:
            queryset = queryset.filter(effect_type=effect_type)
        
        return queryset

class PassiveSkillsView(generics.ListAPIView):
    """
    GET /api/v1/skills/passive/ → Liste aller passiven Skills
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PassiveSkillSerializer
    queryset = Skill.objects.filter(is_active=True, skill_type='passive')

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter nach Layer
        layer = self.request.query_params.get('layer')
        if layer:
            queryset = queryset.filter(layer=layer)
        
        # Filter nach Kategorie
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter nach Buff-Typ
        buff_type = self.request.query_params.get('buff_type')
        if buff_type:
            queryset = queryset.filter(buff_type=buff_type)
        
        # Filter nach Trigger-Bedingung
        trigger_condition = self.request.query_params.get('trigger_condition')
        if trigger_condition:
            queryset = queryset.filter(trigger_condition=trigger_condition)
        
        return queryset

class SkillDetailView(generics.RetrieveAPIView):
    """
    GET /api/v1/skills/{skill_id}/ → Detailansicht eines Skills
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SkillSerializer
    queryset = Skill.objects.filter(is_active=True)

class SkillCreateView(generics.CreateAPIView):
    """
    POST /api/v1/skills/create/ → Neuen Skill erstellen (Admin)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SkillCreateSerializer
    queryset = Skill.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Validiere die Skill-Daten
        skill = serializer.save()
        
        # Verwende den passenden Serializer für die Antwort
        if skill.skill_type == 'active':
            response_serializer = ActiveSkillSerializer(skill)
        elif skill.skill_type == 'passive':
            response_serializer = PassiveSkillSerializer(skill)
        else:
            response_serializer = SkillSerializer(skill)
        
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class UserActiveSkillsView(generics.ListAPIView):
    """
    GET /api/v1/skills/unlocked/active/ → Alle freigeschalteten aktiven Skills des Users
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSkillSerializer

    def get_queryset(self):
        return get_user_skills(self.request.user).filter(skill__skill_type='active')

class UserPassiveSkillsView(generics.ListAPIView):
    """
    GET /api/v1/skills/unlocked/passive/ → Alle freigeschalteten passiven Skills des Users
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSkillSerializer

    def get_queryset(self):
        return get_user_skills(self.request.user).filter(skill__skill_type='passive')
