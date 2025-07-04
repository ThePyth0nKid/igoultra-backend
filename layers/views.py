from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Layer, UserLayerProgress
from .serializers import LayerSerializer, UserLayerProgressSerializer

# Create your views here.

class LayerListView(generics.ListAPIView):
    queryset = Layer.objects.all().order_by('type', 'order')
    serializer_class = LayerSerializer
    permission_classes = [permissions.AllowAny]

class MyUserLayerProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            progress = UserLayerProgress.objects.get(user=request.user)
        except UserLayerProgress.DoesNotExist:
            return Response({'detail': 'No progress found.'}, status=404)
        serializer = UserLayerProgressSerializer(progress)
        return Response(serializer.data)
