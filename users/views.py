from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

import boto3
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from datetime import datetime
from .models import User
from .serializers import UserSerializer
import uuid
from .forms import ProfileCompletionForm
from rest_framework import filters
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions


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


class AvatarS3PresignView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file_name = request.data.get("file_name")
        file_type = request.data.get("file_type")
        folder = request.data.get("folder", "avatars")
        if not file_name or not file_type:
            return Response({"error": "file_name and file_type are required."}, status=status.HTTP_400_BAD_REQUEST)
        # Use user id and uuid for uniqueness
        key = f"{folder}/{request.user.id}_{uuid.uuid4().hex}_{file_name}"
        aws_access_key_id = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
        aws_secret_access_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
        aws_storage_bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
        aws_region_name = getattr(settings, 'AWS_REGION_NAME', None)
        if not all([aws_access_key_id, aws_secret_access_key, aws_storage_bucket_name, aws_region_name]):
            return Response({"error": "AWS S3 settings are missing. Please set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, and AWS_REGION_NAME in your settings."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region_name
        )
        presigned_post = s3.generate_presigned_post(
            Bucket=aws_storage_bucket_name,
            Key=key,
            Fields={"Content-Type": file_type},
            Conditions=[{"Content-Type": file_type}],
            ExpiresIn=3600
        )
        # Überschreibe das 'url'-Feld mit der region-spezifischen URL
        presigned_post['url'] = f"https://{aws_storage_bucket_name}.s3.{aws_region_name}.amazonaws.com/"
        url = f"https://{aws_storage_bucket_name}.s3.{aws_region_name}.amazonaws.com/{key}"
        return Response({"data": presigned_post, "url": url, "key": key})

class AvatarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Return the current avatar_url for the user
        return Response({"avatar_url": request.user.avatar_url})

    def patch(self, request):
        # Set the avatar_url after successful S3 upload
        avatar_url = request.data.get("avatar_url")
        if not avatar_url:
            return Response({"error": "avatar_url is required."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.avatar_url = avatar_url
        request.user.save(update_fields=["avatar_url"])
        return Response({"avatar_url": avatar_url})

    def delete(self, request):
        avatar_url = request.user.avatar_url
        if not avatar_url:
            return Response({"detail": "No avatar to delete."}, status=status.HTTP_400_BAD_REQUEST)
        aws_access_key_id = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
        aws_secret_access_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
        aws_storage_bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
        aws_region_name = getattr(settings, 'AWS_REGION_NAME', None)
        if not all([aws_access_key_id, aws_secret_access_key, aws_storage_bucket_name, aws_region_name]):
            return Response({"error": "AWS S3 settings are missing. Please set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, and AWS_REGION_NAME in your settings."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Extract S3 key from URL
        try:
            bucket = aws_storage_bucket_name
            region = aws_region_name
            prefix = f"https://{bucket}.s3.{region}.amazonaws.com/"
            if not avatar_url.startswith(prefix):
                return Response({"error": "Invalid avatar URL."}, status=status.HTTP_400_BAD_REQUEST)
            key = avatar_url[len(prefix):]
            s3 = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region_name
            )
            s3.delete_object(Bucket=bucket, Key=key)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        request.user.avatar_url = None
        request.user.save(update_fields=["avatar_url"])
        return Response({"detail": "Avatar deleted."}, status=status.HTTP_204_NO_CONTENT)


class IsStaffPermission(permissions.BasePermission):
    """Erlaubt nur is_staff-Usern den Zugriff."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsStaffPermission]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["username", "ultra_name", "email"]
    filterset_fields = ["is_active", "is_staff", "faction", "origin"]
    ordering_fields = ["date_joined", "last_login", "username", "ultra_name"]
