from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Origin
from users.serializers import OriginShortSerializer
from rest_framework.permissions import AllowAny

# Create your views here.

class OriginListView(ListCreateAPIView):
    queryset = Origin.objects.all()
    serializer_class = OriginShortSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Verhindere Dubletten (case-insensitive)
        name = serializer.validated_data["name"].strip()
        obj, created = Origin.objects.get_or_create(
            name__iexact=name,
            defaults={
                "name": name,
                "description": serializer.validated_data.get("description", ""),
                "type": serializer.validated_data.get("type", "Benutzerdefiniert")
            }
        )
        return obj
