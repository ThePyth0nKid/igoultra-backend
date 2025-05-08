from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes

from .forms import ProfileCompletionForm
from .serializers import UserSerializer


@ensure_csrf_cookie
@api_view(["GET"])
@permission_classes([AllowAny])
def get_csrf_token(request):
    """
    Simple endpoint to set the CSRF cookie for the frontend.
    """
    return Response({"detail": "CSRF cookie set"})


@login_required
def complete_profile(request):
    """
    🔧 [LEGACY] HTML-based profile completion view (admin-only or fallback).
    Can be removed once onboarding is fully handled in the frontend.
    """
    if request.method == "POST":
        form = ProfileCompletionForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')  # Optional: redirect to /dashboard
    else:
        form = ProfileCompletionForm(instance=request.user)

    return render(request, 'users/complete_profile.html', {'form': form})


class MeView(APIView):
    """
    🔁 API view to GET and PATCH the authenticated user's data.
    Used by the React frontend: /api/v1/auth/me/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        📥 Return user data (e.g. username, ultra_name, XP, etc.)
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """
        ✏️ Update specific user fields (e.g. ultra_name) via PATCH.
        """
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
