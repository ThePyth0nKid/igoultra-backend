from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Faction
from users.serializers import FactionShortSerializer

# Create your views here.

class FactionListView(ListAPIView):
    queryset = Faction.objects.all()
    serializer_class = FactionShortSerializer
