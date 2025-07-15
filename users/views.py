from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer
from .forms import ProfileCompletionForm


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
            # Nach dem Speichern: User neu laden, um alle Felder aktuell zu haben
            user = type(request.user).objects.get(pk=request.user.pk)
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        🗑️ Löscht das eigene Benutzerkonto des eingeloggten Users.
        """
        user = request.user
        user.delete()
        return Response({"detail": "Account deleted."}, status=status.HTTP_204_NO_CONTENT)


class AvatarUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        user = request.user
        avatar_file = request.FILES.get('avatar')
        if not avatar_file:
            return Response({"error": "Kein Avatar-Bild hochgeladen."}, status=status.HTTP_400_BAD_REQUEST)
        user.avatar = avatar_file
        user.save()  # Erst speichern!
        user.avatar_url = request.build_absolute_uri(user.avatar.url)  # Dann URL setzen!
        user.save()
        return Response({"avatar": user.avatar_url}, status=status.HTTP_200_OK)


class IsStaffPermission(permissions.BasePermission):
    """Erlaubt nur is_staff-Usern den Zugriff."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsStaffPermission]
    search_fields = ["username", "ultra_name", "email"]
    filterset_fields = ["is_active", "is_staff", "faction", "origin"]
    ordering_fields = ["date_joined", "last_login", "username", "ultra_name"]
